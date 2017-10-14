# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Record automatically a negation for a product on a sale',
    'description': '''Records automatically a negation (product_negation) for a
    product that is intended to be sold but has no stock.''',
    'version': '9.0.1.0.0',
    'category': 'Sales',
    'author': 'Humanytek',
    'website': "http://www.humanytek.com",
    'license': 'AGPL-3',
    'depends': [
        'sale_stock',
        'sale_stock_dates_next_receptions',
        'product_rejected'],
    'data': [
    ],
    'installable': True,
    'auto_install': False
}
