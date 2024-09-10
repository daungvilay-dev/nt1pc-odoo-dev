


from odoo import api, fields,models,_

class Property(models.Model):
    _name = "estate.property"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Real Estate Property"
    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    price = fields.Float(string='Price')
    bedrooms = fields.Integer(string='Bedrooms')
    bathrooms = fields.Integer(string='Bathrooms')
    garage = fields.Boolean(string='Aarage')
    area = fields.Float(string='Area')
    location = fields.Char(string='Location')
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    
    
    # @api.depends_context('uid')
    # def _compute_description(self):
    #     print(f'self.env.context')
        # for rec in self:
            # if rec.name :
            #     rec.name = f'{rec.name} - {rec.location}'
            # else:
            #     rec.name = 'sew'
            
    
    # [THIS FOR CONCEPT BUTTON]
    @api.depends('offer_count')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('reject', 'Reject'),
        ('sold', 'Sold'),
        ('cancel', 'Cancelled')
    ], string='Approval Status', default='new', )
    
    def action_sold(self):
        self.state = 'sold'
    def action_cancel(self):
        self.state = 'cancel'
    
    offer_count = fields.Integer(string='Offer Count')
    
    # [THIS FOR CONCEPT BUTTON]
    
    section_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('condo', 'Condo'),
        ('land', 'Land'),
        ('commercial', 'Commercial')
    ], string='Section Type')
    
    
    # [ tracking=True] this one for use tracking field if change or value change it will be show in chatter
    expected_price = fields.Float(string='Expected Price', tracking=True)
    best_offer = fields.Float(string='Best Offer', compute='_compute_best_offer')
    selling_price = fields.Float(string='Selling price', readonly=True)
    date_available_from = fields.Date(string='Date Available From')
    
    sale_id = fields.Many2one('res.users', string='Saleman')
    
     # The 'domain' attribute is used to filter the available options for the 'buyer_id' field.
    # In this case, it restricts the options to only those partners that have 'is_company' set to True.
    buyer_id = fields.Many2one('res.partner', string='Buyer', placeholder='Buyer here' ,  domain=[('is_company','=',True)] )
    
    #get value from object buyer_id for show [relates field with model res.partner]
    buyer_phone = fields.Char(string='Buyer Phone', related='buyer_id.phone', store=True)
    
    
    
    
    @api.depends('bedrooms', 'bathrooms')
    def _compute_total_bedrooms(self):
        for record in self:
            record.total_b_room = record.bedrooms + record.bathrooms

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer =0.0 
    
            
            
            
    total_b_room = fields.Float(string='Total Bedrooms', visiable='1', compute=_compute_total_bedrooms)
    
    
 
 
 
    
        # [
        #   ->[ reload ]  'tag': 'reload',
        #   ->[ notification ]  # 'tag': 'display_notification',
                                # 'params':{
                                #     'title': _('Testing Notification'),
                                #     'type':'success',
                                # }
        # ]
    
    def action_client_action(self):

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params':{
                'title': _('Testing Notification'),
                'type':'success',
            }
        }
    def _get_report_base_filename(self):
        self.ensure_one()
        return "Estate Property Report - %s" % self.name
    
    
    
    
    # this one 'email_template_new_property_listing' get from [data/mail_template.xml] for send mail action
    # this one 'action_send_mail' get from view/property.xml
    def action_send_mail(self):
        mail_template = self.env.ref('real_estate_ads.email_template_new_property_listing')
        mail_template.send_mail(self.id, force_send=True)
   
    email_recipients = fields.Char(compute='_compute_email_recipients', store=True)

    def _get_emails(self):
        return ','.join(self.offer_ids.mapped('partner_mail_send'))

    @api.depends('offer_ids.partner_mail_send')
    def _compute_email_recipients(self):
        for record in self:
            record.email_recipients = record._get_emails()