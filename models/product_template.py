from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    send_to_kitchen = fields.Boolean(
        string='Enviar a Cocina',
        default=False,
        help='Si está marcado, este producto aparecerá en la comanda de cocina'
    )
    
    kitchen_category = fields.Selection([
        ('food', 'Comida'),
        ('beverage', 'Bebida'),
        ('dessert', 'Postre'),
        ('other', 'Otro')
    ], string='Categoría de Cocina', default='food')
    
    preparation_time = fields.Integer('Tiempo de Preparación (min)', default=10)
