{
    'name': 'POS Kitchen Order System',
    'version': '17.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Sistema automático de comandas de cocina para POS',
    'description': """
        Sistema completo de gestión de comandas de cocina:
        - Impresión automática al validar pago
        - Botón de reimpresión de comandas
        - Historial de comandas impresas
        - Configuración por categorías de productos
    """,
    'author': 'ARMKU LLC',
    'depends': ['point_of_sale', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_config_views.xml',
        'views/kitchen_order_views.xml',
        'views/product_views.xml',
        'report/kitchen_order_report.xml',
        'report/kitchen_order_template.xml',
        'data/pos_data.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_kitchen_order/static/src/js/payment_screen.js',
            'pos_kitchen_order/static/src/js/kitchen_button.js',
            'pos_kitchen_order/static/src/js/models.js',
            'pos_kitchen_order/static/src/xml/kitchen_button.xml',
            'pos_kitchen_order/static/src/css/kitchen_order.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
