# -*- coding: utf-8 -*-

from odoo import models, fields, api


class custom_employee(models.Model):
    _inherit = 'hr.employee'
    _description = 'custom_employee.custom_employee'

    # Adding a custom field
    custom_field = fields.Char(string="Custom Field", help="This is a custom field for the employee")
    custom_field1 = fields.Char(string="Custom Field", help="This is a custom field for the employee")

