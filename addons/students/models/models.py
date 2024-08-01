# -*- coding: utf-8 -*-

import time
from odoo import models, fields, api

# from . import friends



# Common Field Types:
        # Char: A string field.
        # Text: A longer text field.
        # Integer: An integer field.
        # Boolean: A boolean (true/false) field.
        # Float: A floating-point number field.
        # Date: A date field.
        # Datetime: A date and time field.
        # Many2one: A many-to-one relationship.
        # One2many: A one-to-many relationship.
        # Many2many: A many-to-many relationship.

class students(models.Model):
    _name = 'st.students'
    _description = 'st.students'

    name = fields.Char(string="Friend Name", placeholder="Please input a name")
    
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    student_lastname = fields.Char(string="Student Lastname", required=True, default="Student")
    student_identifier = fields.Char(string="Student Identifier", readonly=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ])
    advance_gender = fields.Selection('_advance_gender')

    roll_namber = fields.Integer(help="Roll number please use a positive")

    student_data = fields.Json()




    # joining_date = fields.Date(default=fields.Date.today())
    # joining_date = fields.Date(default=fields.Date.today)
    joining_date = fields.Date(default=fields.Date.context_today)

    room_ids = fields.Many2one(comodel_name='rm.room', string="Room")

    friend_ids = fields.Many2one('st.friends',  string="Friend",)
    # room_ids = fields.Many2one('rm.room', string="Room")

    hobby_list = fields.Many2many("st.hobby","student_hobby_relation","student_id","hobby_id", string="Hobbies")



     # compute
    student_fees = fields.Float(string="Student Fees",default=3.2, help="Please enter a student fees for the student")
    discount = fields.Float(string="Discount")

    final_fees = fields.Float("Final fees", compute='final_fees_compute',readonly=True,store=True)



    start_date = fields.Date(default=time.strftime("%Y-01-01"))
    end_date = fields.Date(default=time.strftime("%Y-12-31"))

    duration_days = fields.Integer(string="Duration (days)", compute="_compute_duration_days")
    
    datetime =  fields.Datetime(placeholder="please use a datetime")



    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        for record in self:
            if record.start_date and record.end_date:
                start = fields.Date.from_string(record.start_date)
                end = fields.Date.from_string(record.end_date)
                record.duration_days = (end - start).days
            else:
                record.duration_days = 0

    @api.model
    def _get_gender_vip(self):
        return [
        ('a', 'a VIP'),
        ('b', 'b VIP'),
        ('c', 'c VIP'),
        ]


    advance_gender_vip = fields.Selection(_get_gender_vip)




    def _advance_gender(self):
        return [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ]
    @api.onchange('student_fees', 'discount')
    def _compute_final_fees(self):
        for record in self:
            record.final_fees = record.student_fees - record.discount

    
    def student_data_json(self):
        self.student_data = {"name":self.name,"lastname":self.student_lastname,}
    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100

