# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing


from odoo import models, fields, api, exceptions, _, SUPERUSER_ID
from datetime import datetime,timedelta

class HrEmployee(models.Model):



    _inherit = 'hr.employee'
    
    overtime_ids = fields.One2many('hr.overtime', 'employee_id', string='Overtimes')
    
    def get_overtime_hours(self, emp_id, date_from, date_to=None):
        if date_to is None:
            date_to = datetime.now().strftime('%Y-%m-%d')
        self._cr.execute("SELECT sum(o.number_of_hours) from hr_overtime as o where \
                            o.include_payroll IS TRUE and o.employee_id=%s \
                            and o.state='validate' AND to_char(o.date_to, 'YYYY-MM-DD') >= %s AND to_char(o.date_to, 'YYYY-MM-DD') <= %s ",
                            (emp_id, date_from, date_to))
        res = self._cr.fetchone()
        return res and res[0] or 0.0

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
