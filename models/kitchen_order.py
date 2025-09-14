from odoo import models, fields, api
from datetime import datetime

class KitchenOrder(models.Model):
    _name = 'pos.kitchen.order'
    _description = 'Historial de Comandas de Cocina'
    _order = 'create_date desc'
    
    name = fields.Char('Número de Comanda', required=True, readonly=True)
    pos_order_id = fields.Many2one('pos.order', 'Orden POS', required=True)
    session_id = fields.Many2one('pos.session', 'Sesión', related='pos_order_id.session_id')
    
    # Información de la orden
    order_date = fields.Datetime('Fecha/Hora', default=fields.Datetime.now)
    table_id = fields.Many2one('restaurant.table', 'Mesa')
    customer_name = fields.Char('Cliente')
    user_id = fields.Many2one('res.users', 'Cajero', required=True)
    
    # Estado
    state = fields.Selection([
        ('pending', 'Pendiente'),
        ('printed', 'Impresa'),
        ('prepared', 'Preparada'),
        ('delivered', 'Entregada'),
        ('cancelled', 'Cancelada')
    ], default='pending', string='Estado')
    
    # Líneas de productos
    line_ids = fields.One2many('pos.kitchen.order.line', 'kitchen_order_id', 'Productos')
    
    # Contadores
    print_count = fields.Integer('Veces Impresa', default=0)
    last_print_date = fields.Datetime('Última Impresión')
    
    # Notas
    notes = fields.Text('Notas de Cocina')
    
    @api.model
    def create_from_pos_order(self, order):
        """Crear comanda desde orden POS"""
        kitchen_lines = []
        for line in order.lines:
            if line.product_id.send_to_kitchen:
                kitchen_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'qty': line.qty,
                    'notes': line.customer_note or '',
                }))
        
        if kitchen_lines:
            return self.create({
                'name': f"K-{order.name}",
                'pos_order_id': order.id,
                'table_id': order.table_id.id if order.table_id else False,
                'customer_name': order.partner_id.name if order.partner_id else 'Cliente General',
                'user_id': order.user_id.id,
                'line_ids': kitchen_lines,
                'notes': order.note or '',
            })
        return False
    
    def print_kitchen_order(self):
        """Imprimir comanda"""
        self.print_count += 1
        self.last_print_date = fields.Datetime.now()
        self.state = 'printed'
        
        return self.env.ref('pos_kitchen_order.action_report_kitchen_order').report_action(self)
    
    def mark_as_prepared(self):
        """Marcar como preparada"""
        self.state = 'prepared'
    
    def mark_as_delivered(self):
        """Marcar como entregada"""
        self.state = 'delivered'

class KitchenOrderLine(models.Model):
    _name = 'pos.kitchen.order.line'
    _description = 'Línea de Comanda de Cocina'
    
    kitchen_order_id = fields.Many2one('pos.kitchen.order', 'Comanda', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Producto', required=True)
    qty = fields.Float('Cantidad', required=True)
    notes = fields.Text('Notas/Modificaciones')
