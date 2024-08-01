from xml.dom import ValidationErr
from odoo import models, fields, api

class LifeCycleModel(models.Model):
    _name = 'lifecycle'
    _description = 'Lifecycle'

    name = fields.Char(string='Name', required=True)
    price = fields.Float(string='Price')
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The product name must be unique.')
    ]
    active = fields.Boolean(string='Active', default=True)

   # Initialization (similar to Vue's created):
       # Model Initialization: When a model is defined, you can set default values, define fields, and set up the model.
       # Record Creation: The create method is called when a new record is being created.
    @api.model
    def create(self, vals):
        # Custom logic before record creation
        record = super(LifeCycleModel, self).create(vals)
        # Custom logic after record creation
        return record


    # Reading (similar to Vue's mounted):
       # Record Reading: The read or search methods are used to fetch records from the database.
    @api.model
    def get_records(self):
        records = self.search([])
        for record in records:
            print(record.name, record.description)



    #Deletion (similar to Vue's destroyed):
       #Record Deletion: The unlink method is called when a record is being deleted.
    def unlink(self):
        # Custom logic before record deletion
        res = super(LifeCycleModel, self).unlink()
        # Custom logic after record deletion
        return res
    
    @api.onchange('price')
    def _onchange_price(self):
        if self.price:
            self.discount = self.price * 0.1



    #Compute Methods: Used to compute the value of fields based on other fields.
    discount_price = fields.Float(string='Discount Price', compute='_compute_discount_price')
    @api.depends('price')
    def _compute_discount_price(self):
        for record in self:
            record.discount_price = record.price * 0.9