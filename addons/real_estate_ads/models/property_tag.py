from  odoo import models,fields


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Type"
    
    name = fields.Char(string='Name', required=True)
    color = fields.Char(string='color')