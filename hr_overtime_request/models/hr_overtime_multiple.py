# -*- coding: utf-8 -*-
#########################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP SA (<http://www.odoo.com>)
#    Copyright (C) 2014-TODAY Probuse Consulting Service Pvt. Ltd. (<http://probuse.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################################

import time
from datetime import datetime, timedelta

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import except_orm, Warning, RedirectWarning


Datetime_FORMAT = '%Y-%m-%d'

class hr_overtime_multiple(models.Model):
    _name = 'hr.overtime.multiple'
    _description = 'Employee Overtime Multiple'
    
    _rec_name = 'date_from'
    
    @api.multi
    def unlink(self):
        for request in self:
            if request.state not in ('draft', 'cancel'):
                raise Warning(_('You cannot delete an multiple overtime request which is not draft or cancelled.'))
        return super(hr_overtime_multiple, self).unlink()
    
    @api.model
    def _employee_get(self):
        ids = self.env['hr.employee'].search([('user_id', '=', self._uid)], limit=1)
        if ids:
            return ids
    
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(string='Description', required=False, states={'validate':[('readonly', True)]})
    number_of_hours = fields.Float(string='Number Of Hours', states={'validate':[('readonly', True)]}, store=True)
    include_payroll = fields.Boolean(string='Include In Payroll', states={'validate':[('readonly', True)]}, help='Tick if you want to include this overtime in employee payroll', default=True)
    state = fields.Selection(selection=[('draft', 'ร่าง'),
                                       ('validate', 'ส่งขออนุมัติ')
                                        ],
                                string='Status', readonly=True, default='draft', track_visibility='onchange')
    user_id = fields.Many2one('res.users' ,string='User', default=lambda self: self.env.user)
    date_from = fields.Datetime(string='Start Date', readonly=False, states={'validate':[('readonly', True)]}, default=fields.datetime.now()) 
    date_to = fields.Datetime(string='End Date', readonly=False, states={'validate':[('readonly', True)]})
    approve_date = fields.Date(string='Department Approved Date', readonly=True, copy=False)
    hr_approve_date = fields.Date(string='Approved Date', readonly=True, copy=False)
    employee_ids = fields.Many2many('hr.employee', 'employee_overtime_multiple_rel','employee_id','overtime_id' ,string="Select Employees", required=True,states={'validate':[('readonly', True)]})
    manager_id = fields.Many2one('hr.employee', 'Manager', readonly=False, states={'validate':[('readonly', True)]}, help='This area is automatically filled by the user who will approve the request', copy=False)
    notes = fields.Text(string='Notes',)
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    category_id = fields.Many2one('hr.employee.category', string="Category", readonly=False, states={'validate':[('readonly', True)]}, help='Category of Employee')
    ot_type = fields.Many2one('type.ot', string='ประเภทการทำงานล่วงเวลา')

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=False, states={'validate':[('readonly', True)]},default=lambda self: self.env['res.company']._company_default_get('hr.overtime.multiple'))
    approve_hr_manager_id = fields.Many2one('res.users', string='Approved By', readonly=True, copy=False)
    approve_dept_manager_id = fields.Many2one('res.users', string='Department Manager', readonly=True, copy=False)
    department_manager_id = fields.Many2one('hr.employee', string='Department Manager(RR)')
    
    
    @api.onchange('department_id')
    def onchange_department(self):
        self.department_manager_id = self.department_id.manager_id and self.department_id.manager_id.id or False
    
    
    @api.onchange('date_from')
    def onchange_start_date(self):
        if self.date_to and self.date_from:
            date_start = datetime.strptime(self.date_from, "%Y-%m-%d %H:%M:%S")
            date_end = datetime.strptime(self.date_to, "%Y-%m-%d %H:%M:%S")
            diff_hours = date_end - date_start
            self.number_of_hours = (diff_hours.seconds / 3600.00) + (diff_hours.days * 24.00)
        else:
            self.number_of_hours = 0.0
    
    @api.onchange('date_to')
    def onchange_end_date(self):
        if self.date_to and self.date_from:
            date_start = datetime.strptime(self.date_from, "%Y-%m-%d %H:%M:%S")
            date_end = datetime.strptime(self.date_to, "%Y-%m-%d %H:%M:%S")
            diff_hours = date_end - date_start
            self.number_of_hours = (diff_hours.seconds / 3600.00) + (diff_hours.days * 24.00)
        else:
            self.number_of_hours = 0.0
    
    @api.multi
    def set_to_draft(self):
        self.write({
            'state': 'draft',
            'approve_date': False,
            'hr_approve_date': False,
            'approve_hr_manager_id': False,
            'approve_dept_manager_id' : False
        })
        return True
    
    @api.multi
    def ot_refuse(self):
        obj_emp = self.env['hr.employee']
        ids2 = obj_emp.search([('user_id', '=', self._uid)], limit=1)
        manager = ids2 or False
        self.write({'state': 'refuse', 'manager_id':  manager and manager.id or False})
        return True


    @api.multi
    def ot_cancel(self):
        self.write({'state': 'cancel'})
        return True
    
    @api.multi
    def ot_confirm(self):

        if self.employee_ids:
            for employee in self.employee_ids:
                self.env['hr.overtime'].create({
                'employee_id': employee.id,
                'name': employee.name,
                'date_from' :  self.date_from,
                'date_to' : self.date_to,
                'approve_date' :  self.approve_date,
                'hr_approve_date' :  self.hr_approve_date,
                'manager_id' : self.manager_id and self.manager_id.id or False,
                'notes' : self.notes,
                'category_id': self.category_id,
                'ot_type':self.ot_type.id,
                'company_id': self.company_id.id,
                'approve_hr_manager_id': self.approve_hr_manager_id.id,
                'approve_dept_manager_id' : self.approve_dept_manager_id.id,
                'state' : 'confirm',
                'include_payroll': True,
                'number_of_hours' : self.number_of_hours,
                'multiple_overtime_id' : self.id
        })
                self.write({'state': 'validate'})


        return True        

    @api.multi
    def department_approval(self):
        return self.write({'state':'approve_by_department', 'approve_hr_manager_id': self.env.user.id, 'hr_approve_date': time.strftime('%Y-%m-%d')})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
