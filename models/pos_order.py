# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    kitchen_order_ids = fields.One2many('pos.kitchen.order', 'pos_order_id', 'Kitchen Orders')
    kitchen_order_printed = fields.Boolean('Kitchen Order Printed', default=False)
