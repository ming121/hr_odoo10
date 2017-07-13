# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class report_overtime(models.TransientModel):
    _name = "report.overtime"
    _description = "Report Overtime"


    department_ids = fields.Many2one('hr.department', string='Department', required=True)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')


    def _build_contexts(self, data):
        result = {}
        result['department_ids'] = 'department_ids' in data['form'] and data['form']['department_ids'] or False
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['strict_range'] = True if result['date_from'] else False
        return result
    #
    def _print_report(self, data):
        raise (_('Error!'), _('Not implemented.'))
    #
    @api.multi
    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'department_ids'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'en_US'))
        return self._print_report(data)
