from odoo import models, api


class EmailProxyMixin(models.AbstractModel):
    _name = 'email.proxy.mixin'
    _description = 'Email Proxy Mixin'

    _MODEL_TO_EMAIL_FIELD_MAPPING = {
        'res.partner': 'email',
        'hr.employee': 'work_email',
        'res.company': 'email',
        'res.bank': 'email',
    }
    _NO_MODEL_NAME_IN_DICT_ERROR = '''
        Please supply _MODEL_NAME_TO_EMAIL_FIELD_NAME_MAPPING class attribute
        of email.proxy.mixin model with the model name and name of the field
        that contains email to ensure correct mapping. Currently the dictionary
        has no mail mapped for model %(model_name)s.
        '''

    @api.model_create_multi
    def create(self, vals_list):
        try:
            email_field_name = self._MODEL_TO_EMAIL_FIELD_MAPPING[self._name]
        except KeyError:
            raise NotImplementedError(
                self._NO_MODEL_NAME_IN_DICT_ERROR % {'model_name': self._name}
            )
        records = super().create(vals_list)
        self.env['email.proxy'].create([{
            'res_id': record.id,
            'res_model': self._name,
            'email': getattr(record, email_field_name, False)
        } for record in records])
        return records

    def write(self, vals):
        records = super().write(vals)
        email_field_name = self._MODEL_TO_EMAIL_FIELD_MAPPING.get(self._name)
        if vals.get(email_field_name):
            self.env['email.proxy'].search(self.__get_generic_domain).write({
                'email': vals[email_field_name],
            })
        return records

    def unlink(self):
        self.env['email.proxy'].search(self.__get_generic_domain).unlink()
        super().unlink()

    def __get_generic_domain(self):
        return [
            ('res_id', 'in', self.ids),
            ('res_model', '=', self._name),
        ]
