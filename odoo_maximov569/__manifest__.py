{
    'name': 'Odoo_maximov569',
    'version': '1.0',
    'depends': ['sale', 'hr'],
    'author': 'Sergey Maximov',
    'installable': True,
    'auto_install': True,
    'application': True,
    'data': [
        'views/sale_order_view.xml',

        'report/inherit_report.xml',
    ],
}