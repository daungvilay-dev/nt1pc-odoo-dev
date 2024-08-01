from xml.dom import ValidationErr
from odoo import models, fields, api

class ProductModel(models.Model):
    _name = 'pd.product'
    _description = 'Product'

    name = fields.Char(string='Name', required=True)
    price = fields.Float(string='Price')
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The product name must be unique.')
    ]
    discount_price = fields.Float(string='Discount Price', compute='_compute_discount_price')

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationErr('Price cannot be negative')
            
    def calculate_discount(self, discount):
        for record in self:
            record.price -= record.price * (discount / 100)



    @api.depends('price')
    def _compute_discount_price(self):
        for record in self:
            record.discount_price = record.price * 0.9