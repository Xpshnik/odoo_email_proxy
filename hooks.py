from psycopg2 import sql
from odoo.api import Environment, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    models_with_emails = env['res.email.mixin']._MODEL_TO_EMAIL_FIELD_MAPPING
    for model, email_field in models_with_emails.items():
        cr.execute(
            sql.SQL('''
                INSERT INTO res_email (email, res_id, res_model,
                create_date, write_date, create_uid, write_uid)
                SELECT {email_field}, id, %(model)s,
                current_timestamp, current_timestamp, create_uid, write_uid
                FROM {table}
                WHERE {email_field} IS NOT NULL;
            ''').format(
                email_field=sql.Identifier(email_field),
                table=sql.Identifier(model.replace('.', '_')),
            ),
            {
                'model': model,
            },
        )

def uninstall_hook(cr, registry):
    cr.execute('DROP TABLE res_email;')
