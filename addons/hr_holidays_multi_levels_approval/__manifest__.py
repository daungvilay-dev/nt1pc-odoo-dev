# -*- encoding: utf-8 -*-
# Baamtu, 2017
# GNU Affero General Public License <http://www.gnu.org/licenses/>
{
    "name" : "Holidays multi levels approval",
    'version': '17.0.1.0.0',
    'license': 'AGPL-3',
    "author" : "Baamtu Senegal",
    'summary': 'Multi-level approval for HR Holidays',
    "category": "Generic Modules/Human Resources",
    'website': 'http://www.baamtu.com/',
    'images': ['static/description/banner.jpg'],
    'depends' : ['base','hr', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee.xml',
        'views/holidays.xml'
        ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
