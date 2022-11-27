import logging
from odoo import models, api


_logger = logging.getLogger(__name__)


class ResEmailMixin(models.AbstractModel):
    _name = 'res.email.mixin'
    _description = 'Email Proxy Mixin'

    _MODEL_TO_EMAIL_FIELD_MAPPING = {
        'res.partner': 'email',
        'hr.employee': 'work_email',
        'res.company': 'email',
        'res.bank': 'email',
    }

    _NO_MODEL_NAME_IN_DICT_ERROR = '''
        Please update _MODEL_NAME_TO_EMAIL_FIELD_NAME_MAPPING dictionary
        of res.email.mixin model with the name of the model you extended
        as well as the name of the field that contains email.
        Currently the dictionary has no email field name mapped
        for model %(model_name)s.
    '''

    def __init__(self, pool, cr):
        init_res = super().__init__(pool, cr)
        # this is how you can extend this mixin for other models:
        # type(self)._MODEL_TO_EMAIL_FIELD_MAPPING.update(
        #    {'model.name': 'email_field_name'}
        #)
        return init_res

    @api.model_create_multi
    def create(self, vals_list):
        email_field_name = self._get_field_name_or_raise_error()
        records = super().create(vals_list)
        self.env['res.email'].create([{
                'res_id': record.id,
                'res_model': self._name,
                'email': getattr(record, email_field_name, False)
            } for record in records
            if getattr(record, email_field_name, False)
        ])
        return records

    def write(self, vals):
        email_field_name = self._get_field_name_or_raise_error()
        res = super().write(vals)
        email_field_value = vals.get(email_field_name, None)
        if email_field_value:
            res_emails = self.env['res.email'].search(self._generic_domain)
            res_emails.write({
                'email': vals[email_field_name],
            })
            self.env['res.email'].create([{
                'res_id': r.id,
                'res_model': self._name,
                'email': getattr(r, email_field_name, False)
            } for r in self if r.id not in res_emails.mapped('res_id')])
        elif email_field_value is not None:
            self.env['res.email'].search(self._generic_domain).unlink()
        return res

    def unlink(self):
        self.env['res.email'].search(self._generic_domain).unlink()
        super().unlink()

    @property
    def _generic_domain(self):
        return [
            ('res_id', 'in', self.ids),
            ('res_model', '=', self._name),
        ]

    @api.model
    def _get_field_name_or_raise_error(self):
        try:
            return self._MODEL_TO_EMAIL_FIELD_MAPPING[self._name]
        except KeyError:
            raise NotImplementedError(self._NO_MODEL_NAME_IN_DICT_ERROR % {
                'model_name': self._name
            })
