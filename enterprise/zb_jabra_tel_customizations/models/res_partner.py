# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    
    arabic_name = fields.Char('Arabic Name')
    arabic_street=fields.Char('Arabic Street')
    arabic_street2=fields.Char('Arabic Street2')
    arabic_city=fields.Char('Arabic City')
    arabic_state=fields.Char('Arabic State')
    arabic_country=fields.Char('Arabic State')
    arabic_zip=fields.Char('Arabic Zip')
    additional_no=fields.Char("Additional Number")
    arabic_building=fields.Char("Building Number")
    arabic_vat=fields.Char("Arabic Vat")
    trading_name=fields.Char('Trading Name')
    trading_name_arabic=fields.Char('Trading Name Arabic')
    # arabic_l10n_sa_edi_plot_identification = fields.Char('Arabic Plot Identification')
    mobile = fields.Char('Mobile', help="Mobile phone number of the contact. Used in various places, such as the partner form and the chatter.")
    
    # def action_balance_confirmation(self):
    #     action = self.env.ref('zb_jabra_tel_customizations.balance_confirmation_wiz_action').sudo().read()[0]
    #     # action['context'] = {
    #     #     'active_model': 'res.partner',
    #     #     'active_ids': self.ids
    #     # }
    #     action['context'] = {
    #         'active_model': 'res.partner',
    #         'active_ids': self.ids,
    #         'default_partner_ids': self.ids,
    #     }
    #     return action