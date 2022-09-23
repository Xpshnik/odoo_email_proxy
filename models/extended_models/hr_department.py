from odoo import fields, models


class Department(models.Model):
    _name = 'hr.department'
    _inherit = ['hr.department', 'email.proxy.mixin']

    email = fields.Char()
