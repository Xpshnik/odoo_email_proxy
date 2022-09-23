from odoo.api import Environment, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    models_with_emails = env['email.proxy.mixin']._MODEL_TO_EMAIL_FIELD_MAPPING
    for model, email_field in models_with_emails.items():
        cr.execute(
            '''
                INSERT INTO res_email (email, res_id, res_model,
                create_date, write_date, create_uid, write_uid)
                SELECT %(email_field)s, id, '%(model)s',
                current_timestamp, current_timestamp, create_uid, write_uid
                FROM %(table)s
                WHERE %(email_field)s IS NOT NULL;
            ''',
            {
                'model': model,
                'email_field': email_field,
                'table': model.replace('.', '_')
            },
        )

def uninstall_hook(cr, registry):
    cr.execute('DROP TABLE res_email;')
