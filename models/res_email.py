from odoo import models, fields


class ResEmail(models.Model):
    _name = 'res.email'
    _description = 'Email proxy'

    email = fields.Char()
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
        for email_proxy in self:
            display_name = self.env[email_proxy.res_model].browse(email_proxy.res_id).display_name
            res.append((email_proxy.id, display_name))
        return res
