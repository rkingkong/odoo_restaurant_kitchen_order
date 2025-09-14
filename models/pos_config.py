# -*- coding: utf-8 -*-
from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    auto_print_kitchen = fields.Boolean(
        string='Auto Print Kitchen Orders',
        default=True,
        help='Automatically print kitchen orders when validating payment'
    )
    
    enable_kitchen_reprint = fields.Boolean(
        string='Enable Kitchen Reprint Button',
        default=True,
        help='Show button to reprint kitchen orders in POS'
    )
