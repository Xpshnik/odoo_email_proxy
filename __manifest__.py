# -*- coding: UTF-8 -*-

{
    'name': 'Email Proxy',
    'author': "Viktor Fedoriv",
    'website': 'https://github.com/Xpshnik/odoo_email_proxy',
    'version': '14.0.0.0.2',
    'description': """ """,

    # any module necessary for this one to work correctly
    'depends': [
        'hr',
        'account',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_department_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}
