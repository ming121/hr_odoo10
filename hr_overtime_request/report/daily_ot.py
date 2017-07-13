# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class ReportMingOt(models.Model):
    _name = "report.ming.ot"
    _auto = False
    _order = 'day_from asc'



    name = fields.Many2one('hr.employee','Employee')
    ot_type = fields.Many2one('type.ot', string='ประเภทการทำงานล่วงเวลา')
    day_from = fields.Datetime('เริ่ม')
    day_ot = fields.Datetime('ถึง')
    notes = fields.Char('notes')
    number_of_hours = fields.Integer('Number of Punch')
    date_from = fields.Date('จากวัน')
    date_to = fields.Date('ถึงวัน')

    @api.model_cr
    def init(self):
        """ Event Question main report """
        tools.drop_view_if_exists(self._cr, 'report_ming_ot')
        self._cr.execute(""" CREATE VIEW report_ming_ot AS (
                SELECT 
                    ho.id as id,
                    ho.employee_id as name,
                    ho.ot_type as ot_type,
                    ho.date_from as day_from ,
                    ho.date_to as day_ot,
                    ho.number_of_hours as number_of_hours,
                    ho.notes as notes
                FROM 
                    hr_overtime ho 
                LEFT JOIN 
                    type_ot ot on ot.id = ho.ot_type
                LEFT JOIN 
                    hr_employee he on he.id = ho.employee_id
                
		        
                order by ho.date_to desc
        )""")
#
#
# class Reportcon(models.Model):
#     _name = "report.con"
#     _auto = False
#     # _order = 'day_from asc'
#
#     date_from =fields.Date('จากวัน')
#     date_to = fields.Date('ถึงวัน')