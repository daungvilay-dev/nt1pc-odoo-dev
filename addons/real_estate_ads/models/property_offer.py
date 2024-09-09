from datetime import timedelta
from  odoo import api, models,fields, _
from odoo.exceptions import ValidationError




# about model [ABSTRACT MODEL, TRRANSIENT MODEL, REGULAR MODEL], 

# In the context of Odoo, a model refers to a class that represents a specific type of data or business object. Models in Odoo are used to define the structure and behavior of the data that will be stored in the database.

# There are three types of models in Odoo:

        # [ ABSTRACT MODEL ]: An abstract model is a base model that cannot be instantiated directly. It serves as a blueprint for other models to inherit from. Abstract models are used to define common fields and methods that can be shared among multiple models.

        # [ TRRANSIENT MODEL ]: A transient model is a temporary model that does not persist in the database. It is used to store data temporarily during a specific session or transaction. Transient models are typically used for wizards or temporary data processing.

        # [ REGULAR MODEL ]: A regular model is a concrete model that represents a real-world entity or concept. It can be instantiated and stored in the database. Regular models are used to define the main data structures in an Odoo application, such as customers, products, orders, etc.

# In the code snippet you provided, [ABSTRACT MODEL, TRANSIENT MODEL, REGULAR MODEL] is a list that likely represents the different types of models used in your Odoo project. Each element in the list corresponds to a specific model class.



# Create [ ABSTRACT MODEL ]:
class AbstractModel(models.AbstractModel):
    _name = 'abstract.model.offer'
    _description = 'My Abstract Model'
    partner_email = fields.Char(string='email', )
    partner_phone = fields.Text(string='phone number')



# โดยทั่วไปโมเดลเหล่านี้ใช้สำหรับวิซาร์ดหรือกล่องโต้ตอบที่ต้องมีการโต้ตอบกับผู้ใช้ และจะถูกละทิ้งหลังการใช้งาน
class TransientModel(models.TransientModel):
    _name = 'offer.price.update.wizard'
    _description = 'My Transient Model'
    partner_email = fields.Char(string='email', )
    partner_phone = fields.Text(string='phone number')
    
    new_price = fields.Integer(string='New Offer Price', required=True, default=12)
    
    @api.model_create_multi
    def update_offer_price(self):
        active_ids = self.env.context.get('active_ids', [])
        offers = self.env['estate.property.offer'].browse(active_ids)
        for offer in offers:
            offer.price_for_model_transient = self.new_price



class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offering"
    
    #set other model to inherit
    _inherit = ['abstract.model.offer']
   
   
#     Scenario: When a new offer is created for a property, the compute_name method will automatically generate a descriptive name for the offer based on the property and partner involved.
#     Example:
#     If property_id is "House A" and partner_id is "John Doe", the name field will be set to "Offer for House A from John Doe". 
    @api.depends('property_id', 'partner_id')
    def compute_name(self):
        for field in self:
            if field.property_id or field.partner_id:
               field.name = f'Offer for {field.property_id.name} from {field.partner_id.name}'
            else:
                field.name = False
                
                
    name = fields.Char(strin="Description", compute=compute_name)
    price = fields.Integer(string='Price',required=True, default=1)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status')
    property_id = fields.Many2one('estate.property', string="Property")

    partner_id = fields.Many2one('res.partner', string="Customer")
    # partner_mail_send [use on property.py]
    partner_mail_send = fields.Char("Customer Partner Mail", related='partner_id.email')
    validity =  fields.Integer('Validity (days)')
    create_date =  fields.Date('Create Date')
    
    price_for_model_transient  =  fields.Integer(string='Price for model transient ',required=True, default=1)
    
    
    @api.model
    def _set_create_date(self):
        """
        Sets the create date for the record to the current date.

        :return: The current date as a `Date` object.
        """
        return fields.Date.today()
    
    def action_accept_offer(self):
        self._validate_accepted_offer()  # Validate that the offer is not already accepted.
        
        if self.property_id:
            self.property_id.write({
                'selling_price': self.price,
                "state":'accepted'
                })
        self.status = 'accepted'
        
    def action_decline_offer(self):
        self.status = 'refused'
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price': 0.0,
                "state":'received'
                })
    
    def _validate_accepted_offer(self):
        
        offer_ids = self.env['estate.property.offer'].search([('property_id', '=', self.property_id.id), ('status', '=', 'accepted')])
        
        if offer_ids:
            raise ValidationError(_('You cannot modify an accepted offer'))
    
    
    
    @api.depends('validity', 'create_date')
    # @api.depends_context('uid')
    def _compute_dateline(self):
        # print(f'self.env.context: {self.env.context}')
        # print(f'self._context: {self._context}')
        # print(f'self.env.context.get("uid"): {self.env.context.get("uid")}')
        for record in self:
            if record.validity and record.create_date:
                record.dateline = record.create_date + timedelta(days=record.validity)
    def _inverse_dateline(self):
        for record in self:
            record.validity = (record.dateline - record.create_date).days
    

    
        # dateline = fields.Date(string='Dateline' , compute='_compute_dateline', inverse='_inverse_dateline', default=_set_create_date, store=True)
    dateline = fields.Date(string='Dateline' , compute=_compute_dateline, inverse='_inverse_dateline', store=True)
    
    
    
    #this method for action when we have to crate about this method [submit]
    @api.model_create_multi
    def create(self, vals_list):
        """
        Overrides the default create method to set the create date for the record.

        :param vals_list: A list of dictionaries containing the values for the records to be created.
        :return: The created records.
        """
        for vals in vals_list:
            print('on show create')
            vals['create_date'] = fields.Date.today()
        return super(PropertyOffer, self).create(vals_list)       
            
    
    #this for query when we have to check from data base native query
    #noted when u update script u have to uninstall app and install again [imm not sure]
    _sql_constraints = [
        ('price', 'CHECK(price >= 1 AND price <= 2000000)', 'Price must be between 1 and 20'),
    ]

            
    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            print(f'rec.dateline: {rec.dateline}')
            if rec.dateline <= rec.create_date or rec.validity < 0:
                raise ValidationError(_('Validity cannot be negative'))
            
    @api.onchange('create_date')
    def _onchange_create_date(self):
        print("onChage")  
        
        
    
    ## [METHOD CRUD OF ODOO]
    
    def write(self, vals):
        """
        Overrides the default write method to set the create date for the record.

        :param vals: A dictionary containing the values to be written.
        :return: The written record.
        """
        print(vals)
        
        print(f'[DETAIL DATABASE CONNECT] {self.env.cr}')
        print(f'[ SHOW ID UESR CURRENT LOGIN] {self.env.uid}')
        print(f'[THIS ONE IS PROVIDES ACCESS TO REGISTRY BY MODEL OR THIS MODEL [estate.property.offer, estate.property] ] {self.env.context}')
        
        #query or core other model for something you want
        get_data_of_parner = self.env['res.partner'].search([('is_company', '=', True )]).filtered(lambda x: x.phone=='(870)-931-0505')
        
        #[YOU CAN YOU CORE ANY WAY LIKE THIS]
        #  --> [ SEARH LIMIT AND ORDER ]  self.env['res.partner'].search([('is_company', '=', True )],limit=1,order='name desc')
        #  --> [ COUNT ] self.env['res.partner'].search_count([('is_company', '=', True )])   
        #  --> [ SEARCH AND DELETE ] self.env['res.partner'].search([('is_company', '=', True )]).unlink()   
        #  --> [ SEARCH THEN MAP ] self.env['res.partner'].search([('is_company', '=', True )]).mapped('phone') #output is ['phone1','phone2']     
        #  --> [ SEARCH THEN FILTER ] self.env['res.partner'].search([('is_company', '=', True )]).filtered(lambda x: x.phone=='(870)-931-0505') #output is ['name1','name2']     
        
        
        #if you use browse you can use ID for finding or filter for get value
        get_data_of_parner_browse = self.env['res.partner'].browse(1) # ouput is res.partner(1,)
        print(get_data_of_parner)
        print(get_data_of_parner_browse)
        return super(PropertyOffer, self).write(vals)
    
    
    def extend_offer_deadline(seft):
        active_ids = seft._context.get('active_ids', [])
        print("active_ids", active_ids)
        if active_ids:
            offer_ids = seft.env['estate.property.offer'].browse(active_ids)
            for offer in offer_ids:
                offer.validity = 10
                
    def _extend_offer_deadline(seft):
            offer_ids = seft.env['estate.property.offer'].search([])
            for offer in offer_ids:
                offer.validity += 1
    
