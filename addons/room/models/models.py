# -*- coding: utf-8 -*-

from odoo import models, fields, api


class room(models.Model):
    _name = 'rm.room'
    _description = 'rm.room'

    name = fields.Char(string="Room Name", required=True)
    room_number = fields.Char(string="Room Number", required=True)

    obj_room = fields.Many2one('obj.room',string='Room object')

    # student_ids = fields.One2many('st.students','room_id')
    # student_ids =  fields.One2many('st.students', 'room_id', string='Student List')

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class objectRoom(models.Model):
    _name = 'obj.room'
    _description = 'obj.room'

    name = fields.Char(string="Room Name", required=True)
    room_ids = fields.One2many('rm.room', 'obj_room', string='Rooms')