#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _



class hr_train(models.Model):
    _name = "hr.train"



    name = fields.Char(string='หัวข้ออบรม', required=True)
    number_of_hours = fields.Float(string='จำนวนเวลา', states={'draft': [('readonly', False)]}, readonly=True,
                                   store=True)
    date_from = fields.Datetime(string='วันที่เริ่มอบรม', states={'draft': [('readonly', False)]}, readonly=True,
                                default=fields.datetime.now())
    date_to = fields.Datetime(string='วันที่สินสุดการอบรม', states={'draft': [('readonly', False)]}, readonly=True)
    department_id = fields.Many2one('employee_name.department_id', string='Department', type='many2one',
                                    relation='hr.department', readonly=True, store=True)
    department_tranning = fields.Char(string='หน่วยงาน อบรม', required=False)
    place_tranning = fields.Selection([('a', 'IN'), ('b', 'OUT')], string="การอบรมภายใน/ภายนอก")
    notes = fields.Text(string='หมายเหตุ')
    employee_name = fields.Many2many('hr.employee', 'employee_tranings', 'employee_id', 'traning_id',
                                     string="Select Employees", required=True,
                                     states={'validate': [('readonly', True)]})
    state = fields.Selection(selection=[('draft', 'สร้าง'),
                                        ('confirm', 'ยืนยันหัวข้ออบรม'),
                                        ('approve_hr', 'ดำเนินงานตามแผน'),
                                        ('refuse', 'ตีกลับ'),
                                        ('validate', 'สิ้นสุดการอบรม'),
                                        ('cancel', 'ยกเลิก')],
                             string='Status', readonly=True, default='draft', track_visibility='onchange')
    approve_dept_manager_id = fields.Many2one('res.users', string='Department Manager', readonly=True, copy=False)
    approve_date = fields.Date(string='Department Approved Date', readonly=True, copy=False)
    agency_traning = fields.Char(string="หน่วยงานจัดอบรม", states={'draft': [('readonly', False)]}, readonly=True,
                                 copy=False)
    traning_venue = fields.Char(string="สถานที่อบรม", states={'draft': [('readonly', False)]}, readonly=True,
                                copy=False)
    expenses_tran = fields.Selection([('0', 'ฟรี'), ('1', 'มีค่าอบรม')], string="ค่าใช้จ่ายในการอบรม", default='0')
    price_tran = fields.Char(string="ราคา")

