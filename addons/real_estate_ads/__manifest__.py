
{
    'name': 'Real Estate Ads',
    'version': '1.0',
    'summary': 'Real Estate Ads Module for Odoo',
    'description': 'This module allows you to manage real estate ads in Odoo.',
    'author': 'Your Name',
    'category': 'Sales',
    'depends': ['base','mail'],
    'data': [
        
        #group 
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'security/model_access.xml',
        'security/ir_rule.xml',
        
        
        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/property_offer_view.xml',
        'views/menu_items.xml',
        
        #data file
          #import by xml file
        #'data/property_type.xml',
          #import by xml csv
        'data/estate.property.type.csv',
         'data/mail_template.xml',
        
        #reports
        "report/property_report.xml",
        "report/report_template.xml",
        
    ],

    
    #demo action after we install module appp only
    "demo":['demo/property_tag.xml'],
'assets': {
    'web.assets_backend': [
        '/web/static/lib/requirejs/require.js',  # Ensure this path is correct
        'real_estate_ads/static/src/js/my_custom_tag.js',
        'real_estate_ads/static/src/xml/my_custom_tag.xml',
    ],
},
    'installable': True,
    'application': True,
    'auto_install': False,
}