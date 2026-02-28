# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.company"
    
    
    
    arabic_name=fields.Char('Arabic Name')
    arabic_street=fields.Char('Arabic Street')
    arabic_street2=fields.Char('Arabic Street2')
    arabic_city=fields.Char('Arabic City')
    arabic_state_id=fields.Char('Arabic State')
    arabic_zip=fields.Char('Arabic Zip')
    arabic_country_id=fields.Char('Arabic Country')
    arabic_vat=fields.Char('Arabic Vat')
    arabic_building=fields.Char('Arabic Building Number')
    trading_name = fields.Char(string='Trading Name', related='partner_id.trading_name', store=True,readonly=False)
    trading_name_arabic = fields.Char(string='Trading Name Arabic', related='partner_id.trading_name_arabic', store=True,readonly=False)
    arabic_l10n_sa_edi_plot_identification = fields.Char('Arabic Plot Identification')
    crn_number = fields.Char('CRN Number')
    balance_confirmation=fields.Char('Balance Confirmation')
    arabic_additional_identification=fields.Char('Arabic Identification Number')
    mobile = fields.Char('Mobile', help="Mobile phone number of the contact. Used in various places, such as the partner form and the chatter.")

    
    
    
   




