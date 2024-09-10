from  odoo import api, models,fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    
    property_id = fields.One2many('estate.property', 'type_id', string='Property')     
    
    
                
    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='description')
    
    
    #create a new field for the property type model 

    
    