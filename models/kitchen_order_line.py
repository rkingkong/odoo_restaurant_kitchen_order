# -*- coding: utf-8 -*-
from odoo import models, fields

class PosKitchenOrderLine(models.Model):
    _name = 'pos.kitchen.order.line'
    _description = 'Kitchen Order Line'
    
    kitchen_order_id = fields.Many2one('pos.kitchen.order', 'Kitchen Order', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    product_name = fields.Char('Product Name', related='product_id.name')
    qty = fields.Float('Quantity', default=1.0, required=True)
    notes = fields.Text('Notes')
