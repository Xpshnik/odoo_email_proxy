from odoo import models


class Bank(models.Model):
    _name = 'res.bank'
    _inherit = ['res.bank', 'res.email.mixin']
