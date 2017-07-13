#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero





class hr_payroll_year(models.Model):
    _name = 'hr.payroll.year'

    name = fields.Char(string='ปีค่าจ้าง', required=True)
    line_ids = fields.One2many('hr.payroll.period', 'period_id',
                               'Perriod')


class hr_payroll_period(models.Model):
    _name = 'hr.payroll.period'

    period_id = fields.Many2one('hr.payroll.year',
                                 'รอบจ่าย',
                                 # ondelete='cascade',
                                 readonly=True)

    payroll_name = fields.Selection([
                                    ('1','ม.ค.'),
                                    ('2','ก.พ.'),
                                    ('3','มี.ค.'),
                                    ('4','เม.ย.'),
                                    ('5','พ.ค.'),
                                    ('6','มิ.ย.'),
                                    ('7','ก.ค.'),
                                    ('8','ส.ค.'),
                                    ('9','ก.ย.'),
                                    ('10','ต.ค.'),
                                    ('11','พ.ย.'),
                                    ('12','ธ.ค.')
                                    ],
                                    string="งวดเดือนจ่าย")
    name = fields.Char(string='รอบจ่าย', required=True)
    date_from = fields.Date('จากวัน')
    date_to = fields.Date('ถึงวัน')



class payroll_money_type(models.Model):
    _name = 'hr.payroll.money.type'

    code = fields.Char(string='รหัส')
    name = fields.Char(string='คำอธิบาย')
    type_pay = fields.Selection ([
                                  ('plus','เพิ่ม'),
                                    ('deduct','หัก')
                                    ],
                                    string="ประเภทเงิน")
#




class payroll_money_plus(models.Model):
    _name = 'hr.payroll.money.plus'

    payroll_money_ids = fields.Many2one('hr.payroll.money.type', ondelete='restrict',
                                   string="รายได้", required=True)
    quantity = fields.Float(string="มูลค่า")
    employee_id = fields.Many2one('hr.employee', string="Employee", select=True, required=True, readonly=True)

class payroll_money_deduct(models.Model):
    _name = 'hr.payroll.money.deduct'

    payroll_money_ids = fields.Many2one('hr.payroll.money.type', ondelete='restrict',
                                        string="รายหัก", required=True)
    quantity = fields.Float(string="มูลค่า")
    employee_id = fields.Many2one('hr.employee', string="Employee", select=True, required=True, readonly=True)




class hr_sso_config(models.Model):
    _name = 'hr.sso.config'


    name = fields.Char(string="รายละเอียด")
    maximun_wage = fields.Float(string='อัตราค่าจ้างสูงสุด', required=True)
    minimun_wage = fields.Float(string='อัตราค่าจ้างต่ำสุด', required=True)
    contribution_rate = fields.Float(string='อัตราเงินสมทบ', required=True)

