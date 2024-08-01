# -*- coding: utf-8 -*-

import time
from odoo import models, fields, api

class hobby(models.Model):
    _name = 'st.hobby'
    _description = 'st.hobby'

    name = fields.Char(string="Hobby Name", placeholder="Please input a name")
    student_ids = fields.One2many('st.students', 'friend_ids', string="Students")
    

