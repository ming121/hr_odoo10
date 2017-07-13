#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp




class Employee(models.Model):

    _inherit = "hr.employee"


    employee_no    = fields.Char(string =  "รหัสพนักงาน")
    name_type = fields.Selection([('m','นาย'),('f','น.ส.'),('fm','นาง')], string="คำนำหน้าชื่อ")
    day_startwroking = fields.Date('วันเริ่มงาน')
    pay = fields.Integer(string ="ค่าจ้าง")
    pay_type = fields.Selection( [('0','รายเดือน'),('1','รายวัน')],string ="รายเดือน/รายวัน")
    with_holding = fields.Integer (string="ภาษีหัก ณ ที่จ่าย",default=0)
    bank_id_name = fields.Char('บัญชีธนาคาร')
    bank_brach_name  = fields.Char('สาขาธนาคาร')
    date_resign = fields.Date('วันออกงาน')
    type_resing = fields.Selection(
                                    [('1','ลาออก'),
                                     ('2','สิ้นสุดระยะเวลาการจ้าง'),
                                     ('3','เลิกจ้าง'),
                                     ('4', 'เกษียนอายุ'),
                                     ('5', 'ไล่ออก/ให้ออกเนื่องจากกระทำผิด'),
                                     ('6', 'ตาย'),
                                     ('7', 'ย้ายสาขา'),]
                                     , string="เหตุที่ออก")

    money_plus_ids = fields.One2many('hr.payroll.money.plus', 'employee_id', string='เงินเพิ่ม ')
    money_deduct_ids = fields.One2many('hr.payroll.money.deduct', 'employee_id', string='เงินหัก ')


