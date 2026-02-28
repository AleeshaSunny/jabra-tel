# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class resCountryState(models.Model):
    _inherit = "res.country.state"
    
    
    arabic_name = fields.Char(index=True, default_export_compatible=True)
    
    
    