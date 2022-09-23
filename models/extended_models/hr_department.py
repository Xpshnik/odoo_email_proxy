from odoo import fields, models


class Department(models.Model):
    _name = 'hr.department'
    _inherit = ['hr.department', 'res.email.mixin']

    email = fields.Char()

    def __init__(self, pool, cr):
        init_res = super().__init__(pool, cr)
        # this is how you can extend res.email.mixin for hr.department
        type(self)._MODEL_TO_EMAIL_FIELD_MAPPING.update({
            self._name: 'email',
        })
        return init_res
