# -*- coding: utf-8 -*-
{
    'name': 'Restaurant Kitchen Order System',
    'version': '17.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Automatic kitchen order printing for POS',
    'description': """
        Kitchen Order Management System for Restaurants
        ================================================
        - Automatic kitchen order printing on payment validation
        - Reprint button for kitchen orders
        - Kitchen order history
        - Product configuration for kitchen items
    """,
    'author': 'ARMKU LLC',
    'website': 'https://armku.us',
    'depends': [
        'point_of_sale',
        'product',
    ],
    'data': [
        # Security DEBE ir DESPUÉS de que los modelos estén cargados
        'security/ir.model.access.csv',
        
        # Data files
        'data/sequence_data.xml',
        
        # Views
        'views/pos_config_views.xml',
        'views/kitchen_order_views.xml',
        'views/product_views.xml',
        
        # Reports
        'report/kitchen_order_report.xml',
        'report/kitchen_order_template.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'odoo_restaurant_kitchen_order/static/src/js/payment_screen.js',
            'odoo_restaurant_kitchen_order/static/src/js/kitchen_button.js',
            'odoo_restaurant_kitchen_order/static/src/xml/kitchen_button.xml',
            'odoo_restaurant_kitchen_order/static/src/css/kitchen_order.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
