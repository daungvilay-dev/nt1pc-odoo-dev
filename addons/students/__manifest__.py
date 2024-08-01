# -*- coding: utf-8 -*-
{
    'name': "students",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Custom Addons/Human Resources",
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','room','teachers'],
    'installable': True,
    'application': True,
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/st_views.xml',
        'views/st_friends.xml',
        'views/templates.xml',
    ],
    
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}

