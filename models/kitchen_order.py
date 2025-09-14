# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime

class PosKitchenOrder(models.Model):
    _name = 'pos.kitchen.order'
    _description = 'Kitchen Order'
    _order = 'create_date desc'
    
    name = fields.Char('Order Number', required=True, readonly=True, default='New')
    pos_order_id = fields.Many2one('pos.order', 'POS Order')
    order_date = fields.Datetime('Order Date', default=fields.Datetime.now)
    table_name = fields.Char('Table')
    customer_name = fields.Char('Customer', default='General Customer')
    user_id = fields.Many2one('res.users', 'Cashier', default=lambda self: self.env.user)
    
    state = fields.Selection([
        ('pending', 'Pending'),
        ('printed', 'Printed'),
        ('prepared', 'Prepared'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], default='pending', string='Status')
    
    line_ids = fields.One2many('pos.kitchen.order.line', 'kitchen_order_id', 'Order Lines')
    
    print_count = fields.Integer('Print Count', default=0)
    last_print_date = fields.Datetime('Last Print Date')
    notes = fields.Text('Kitchen Notes')
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pos.kitchen.order') or 'K-001'
        return super(PosKitchenOrder, self).create(vals)
