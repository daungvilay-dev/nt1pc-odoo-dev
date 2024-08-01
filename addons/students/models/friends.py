# -*- coding: utf-8 -*-

import time
from odoo import models, fields, api

class friends(models.Model):
    _name = 'st.friends'
    _description = 'st.friends'

    name = fields.Char(string="Friend Name", placeholder="Please input a name")
    age = fields.Char(string="Age", placeholder="Please input a age")
    student_ids = fields.One2many('st.students', 'friend_ids', string="Students",)
    

