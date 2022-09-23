from odoo import models


class Company(models.Model):
    _name = 'res.company'
    _inherit = ['res.company', 'res.email.mixin']
