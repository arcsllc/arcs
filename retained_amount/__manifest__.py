# -*- coding: utf-8 -*-
#############################################################################
#
#    Madfox Solutions
#
#    Copyright (C) 2021-TODAY Madfox Solutions(<https://www.madfox.solutions>).
#    Author: Mohamad MOaiad Bashiti (moaiad@madfox.solutions)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    'name': "retained_amount",
    'version': '14.0.1.0.0',

    'summary': """
        arcs modifications for purchase agreement""",

    'description': """
        add percentge to purchase agreement
        add retained amount
        generate tax for purchase agreement
    """,

    'author': "MadFox limited",
    'website': "http://www.madfox.solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/purchase_requistion_form_b.xml'
    ],
    # only loaded in demonstration mode

    'installable': True,
    'application': False,
    'auto_install': True,
}
