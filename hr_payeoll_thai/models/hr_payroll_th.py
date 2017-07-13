# -*- coding: utf-8 -*-

import json
from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang

from odoo.exceptions import UserError, RedirectWarning, ValidationError

import odoo.addons.decimal_precision as dp
import logging

# _logger = logging.getLogger(__name__)



class hr_payroll_th(models.Model):
    _name = "hr.payroll.th"
    _inherit = ['mail.thread']



    name = fields.Char(string="งวด", size=32,
                       track_visibility='onchange')
    period_id = fields.Many2one('hr.payroll.period', string='งวดการจ่าย')
    sso_name = fields.Char(string='เลขที่บัญชี ประกันสังคม')

    branch_sso = fields.Char(string='สาขา')

    comment = fields.Text('Additional Information', readonly=True)



    pay_th_line_ids = fields.One2many('hr.payroll.th.line', 'payroll_line_id', string='Pay Lines')






class hr_payroll_th(models.Model):

    _inherit = ['hr.payroll.th']

    pay_th_lineming = fields.One2many('hr.payroll.th.line', 'payroll_line_id', string='Invoice Lines2', copy=True)














class hr_payroll_th_line(models.Model):
    _name = "hr.payroll.th.line"






    name = fields.Text(string='Description')


    payroll_line_id = fields.Many2one('hr.payroll.th', string='Invoice Reference',
        ondelete='cascade', index=True)
    payroll_line_id2 = fields.Many2one('hr.payroll.th', string='Invoice Reference',
                                      ondelete='cascade', index=True)





    employee_ids = fields.Many2one('hr.employee',ondelete='restrict',
                                    string="Employees", required=True)
    company_id = fields.Many2one('res.company',
                                 related='employee_ids.company_id',
                                 string='Company')

    salary_base = fields.Float(digits=dp.get_precision('Payroll'))
    quantity_day = fields.Float(digits=dp.get_precision('Payroll'),default=1)
    sum_pay = fields.Float(compute='_compute_total', string='Total', digits=dp.get_precision('Payroll'), store=True)
    other_income = fields.Float(string="รายได้อื่น", digits=dp.get_precision('Payroll'), store=True)
    diligence = fields.Float(string="เบี้ขยัน", digits=dp.get_precision('Payroll'), store=True)
    total_receipts = fields.Float(compute='_compute_receipts',string="รายรับรวม", digis=dp.get_precision('Payroll'),store=True)

    @api.multi
    @api.depends('salary_base', 'quantity_day')
    def _compute_total(self):
        for line in self:
            line.sum_pay = float(line.quantity_day * line.salary_base)

    @api.multi
    @api.depends('sum_pay', 'other_income', 'diligence')
    def _compute_receipts(self):
        for line in self:
            line.total_receipts = float(line.sum_pay + line.other_income + line.diligence )

    tax = fields.Float(string="ภาษ๊หัก ณ ที่จ่าย", digits=dp.get_precision('Payroll'), store=True)
    other_broken = fields.Float(string="หัก อื่นๆ", digits=dp.get_precision('Payroll'), store=True)
    amount_sso = fields.Float(
        # compute='_compute_sso',
        string='เงินสมบท', digits=dp.get_precision('Payroll'), store=True)
    rate = fields.Float(string='Rate (%)', digits=dp.get_precision('Payroll Rate'), related='sso_id.contribution_rate',
                        store=True)
    total_deduction = fields.Float(
        # compute='_compute_deduction',
        string="รายการหักรวม", digits=dp.get_precision('Payroll'), store=True)

    pay_total = fields.Float(
        # compute='_compute_pay_total',
        string="สรุปรายได้", digits=dp.get_precision('Payroll'), store=True)

    sso_id = fields.Many2one('hr.sso.config', string='SSO', index=True, copy=False, )



#
# class hr_payroll_th_line_deduction(models.Model):
#     _name = "hr.payroll.th.line.deduction"
#
#
#
#
#
#     payroll_deduction_id = fields.Many2one('hr.payroll.th', string='Invoice Reference',
#                                       ondelete='cascade', index=True)
#
#     employee_ids = fields.Many2one('hr.employee', ondelete='restrict',
#                                    string="Employees", required=True)
#
#     tax = fields.Float(string="ภาษ๊หัก ณ ที่จ่าย", digits=dp.get_precision('Payroll'), store=True)
#     other_broken = fields.Float(string="หัก อื่นๆ", digits=dp.get_precision('Payroll'), store=True)
#     amount_sso = fields.Float(
#                                 # compute='_compute_sso',
#                                 string='เงินสมบท',digits=dp.get_precision('Payroll'),store=True)
#     rate = fields.Float(string='Rate (%)', digits=dp.get_precision('Payroll Rate') ,related='sso_id.contribution_rate',store=True)
#     total_deduction =fields.Float(
#                                     # compute='_compute_deduction',
#                                     string="รายการหักรวม",digits=dp.get_precision('Payroll'),store=True)
#
#     pay_total =fields.Float(
#                                 # compute='_compute_pay_total',
#                                 string="สรุปรายได้",digits=dp.get_precision('Payroll'),store=True)
#
#     sso_id = fields.Many2one('hr.sso.config', string='SSO', index=True, copy=False, )

    # rate_maximun_wage = fields.Float(related='sso_id.maximun_wage', store=True)
    # rate_minimun_wage = fields.Float(related='sso_id.minimun_wage', store=True)
    # rate_sso = fields.Float(string='อัตราเงินสมทบ', related='sso_id.contribution_rate', store=True, copy=False)
    #

    #
    # @api.multi
    # @api.depends('salary_base', 'quantity_day', 'rate','rate_maximun_wage','rate_minimun_wage')
    # def _compute_sso(self):
    #     for line in self:
    #         sum_pay = float((line.quantity_day * line.salary_base))
    #         if  sum_pay <= line.rate_minimun_wage :
    #             self.amount_sso = round(( line.rate_minimun_wage * line.rate) / 100)
    #             return
    #
    #         elif sum_pay  >= line.rate_maximun_wage :
    #             self.amount_sso = round((line.rate_maximun_wage * line.rate) / 100)
    #             return
    #         else  :
    #             self.amount_sso = round( (sum_pay * line.rate )/ 100)
    #             return
    #

    #
    # @api.multi
    # @api.depends('tax', 'other_broken', 'amount_sso')
    # def _compute_deduction(self):
    #     for line in self:
    #         line.total_deduction = float(line.tax + line.other_broken + line.amount_sso )
    #
    # @api.multi
    # @api.depends('total_receipts', 'total_deduction')
    # def _compute_pay_total(self):
    #     for line in self:
    #         line.pay_total = float(line.total_receipts -  line.total_deduction)






