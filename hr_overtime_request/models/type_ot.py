# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource





class type_ot(models.Model):

    _name = "type.ot"
    _description = "ot"

    name = fields.Char(string="ลักษณะการทำงานล่วงเวลา", required=True)
    amount = fields.Char(string="จำนวนเท่า")
    # employee_ids = fields.Many2many('hr.employee', 'employee_category_rel', 'category_id', 'emp_id', string='Employees')

    # _sql_constraints = [
    #     ('name_uniq', 'unique (name)', "Tag name already exists !"),
    # ]