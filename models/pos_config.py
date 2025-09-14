from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    auto_print_kitchen = fields.Boolean(
        string='Comandas de Cocina Automáticas',
        default=True,
        help='Imprimir automáticamente comandas de cocina al validar pagos'
    )
    
    print_kitchen_on_payment = fields.Boolean(
        string='Imprimir al Pagar',
        default=True
    )
    
    enable_kitchen_reprint = fields.Boolean(
        string='Botón de Reimpresión',
        default=True,
        help='Mostrar botón para reimprimir comandas en el POS'
    )
    
    kitchen_categories = fields.Many2many(
        'pos.category',
        string='Categorías de Cocina',
        help='Categorías de productos que se envían a cocina'
    )
