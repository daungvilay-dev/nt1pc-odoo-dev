# -*- coding:utf-8 -*-
from odoo import models, fields, api

class Holidays(models.Model):
    _inherit = "hr.leave"

    def _default_approver(self):
        employee = self.employee_id
        if employee and employee.holidays_approvers:
            return employee.holidays_approvers[0].approver.id

    pending_approver = fields.Many2one('hr.employee', string="Pending Approver", readonly=True, default=_default_approver)
    pending_approver_user = fields.Many2one('res.users', string='Pending approver user', related='pending_approver.user_id', readonly=True)
    current_user_is_approver = fields.Boolean(string='Current user is approver', compute='_compute_current_user_is_approver')
    approbations = fields.One2many('hr.employee.holidays.approbation', 'holidays', string='Approvals', readonly=True)
    pending_transfered_approver_user = fields.Many2one('res.users', string='Pending transfered approver user', compute="_compute_pending_transfered_approver_user", search='_search_pending_transfered_approver_user')

    @api.depends('pending_approver')
    def _compute_current_user_is_approver(self):
        for record in self:
            record.current_user_is_approver = record.pending_approver.user_id.id == self.env.uid

    @api.onchange('employee_id')
    def _onchange_employee(self):
        for record in self:
            if record.employee_id and record.employee_id.holidays_approvers:
                record.pending_approver = record.employee_id.holidays_approvers[0].approver.id
            else:
                record.pending_approver = False

    @api.depends('pending_approver')
    def _compute_pending_transfered_approver_user(self):
        for record in self:
            record.pending_transfered_approver_user = record.pending_approver.transfer_holidays_approvals_to_user

    def _search_pending_transfered_approver_user(self, operator, value):
        employees = self.env['hr.employee'].search([('transfer_holidays_approvals_to_user', operator, value)])
        return [('pending_approver', 'in', employees.ids)]

    def action_confirm(self):
        res = super(Holidays, self).action_confirm()
        for holiday in self:
            if holiday.employee_id.holidays_approvers:
                holiday.pending_approver = holiday.employee_id.holidays_approvers[0].approver.id
        return res

    def action_approve(self):
        for holiday in self:
            is_last_approbation = False
            sequence = 0
            next_approver = None
            for approver in holiday.employee_id.holidays_approvers:
                sequence += 1
                if holiday.pending_approver.id == approver.approver.id:
                    if sequence == len(holiday.employee_id.holidays_approvers):
                        is_last_approbation = True
                    else:
                        next_approver = holiday.employee_id.holidays_approvers[sequence].approver
            if is_last_approbation:
                holiday.action_validate()
            else:
                holiday.write({'state': 'confirm', 'pending_approver': next_approver.id})
                self.env['hr.employee.holidays.approbation'].create({
                    'holidays': holiday.id, 
                    'approver': self.env.uid, 
                    'sequence': sequence, 
                    'date': fields.Datetime.now()
                })
    
    def action_validate(self):
        for holiday in self:
            self.env['hr.employee.holidays.approbation'].create({
                'holidays': holiday.id, 
                'approver': self.env.uid, 
                'date': fields.Datetime.now()
            })
        self.write({'pending_approver': None})
        return super(Holidays, self).action_validate()
