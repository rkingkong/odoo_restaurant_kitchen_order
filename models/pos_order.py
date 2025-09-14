from odoo import models, api

class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    kitchen_order_ids = fields.One2many('pos.kitchen.order', 'pos_order_id', 'Comandas de Cocina')
    
    def action_pos_order_paid(self):
        """Override para crear comanda al pagar"""
        res = super(PosOrder, self).action_pos_order_paid()
        
        # Crear comanda de cocina automáticamente
        for order in self:
            if order.config_id.auto_print_kitchen:
                kitchen_order = self.env['pos.kitchen.order'].create_from_pos_order(order)
                if kitchen_order and order.config_id.print_kitchen_on_payment:
                    kitchen_order.print_kitchen_order()
        
        return res
    
    def print_kitchen_order_manual(self):
        """Imprimir comanda manualmente"""
        kitchen_order = self.env['pos.kitchen.order'].create_from_pos_order(self)
        if kitchen_order:
            return kitchen_order.print_kitchen_order()
