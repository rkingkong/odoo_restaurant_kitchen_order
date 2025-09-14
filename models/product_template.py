# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    send_to_kitchen = fields.Boolean(
        string='Send to Kitchen',
        default=False,
        help='If checked, this product will appear in kitchen orders'
    )
