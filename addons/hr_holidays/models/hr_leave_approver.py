from odoo import api, fields, models

class HrLeaveApprover(models.Model):
    _name = 'hr.leave.approver'
    _description = 'Leave Approver'

    leave_id = fields.Many2one('hr.leave', string='Leave', required=True)
    employee_id = fields.Many2one('hr.employee', string='Approver', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('refused', 'Refused')
    ], string="Status", default='pending')
    
