from odoo import models, fields


class ResEmail(models.Model):
    _name = 'res.email'
    _description = 'Email proxy'

    name = fields.Char(readonly=True)
    email = fields.Char(required=True)
    res_model = fields.Char(
        'Resource Model',
        readonly=True,
        required=True,
    )
    res_id = fields.Many2oneReference(
        'Resource ID',
        model_field='res_model',
        readonly=True,
        required=True,
    )

    def name_get(self):
        res = []
        for res_email in self:
            display_name = self.env[res_email.res_model].browse(res_email.res_id).display_name
            res.append((res_email.id, display_name))
            res_email.name = display_name
        return res
