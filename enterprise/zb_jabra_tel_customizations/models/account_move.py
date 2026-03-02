# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,_,api
import locale
from odoo.exceptions import ValidationError
import io
import base64
import qrcode 
from num2words import num2words

from odoo import models, api, _
from odoo.exceptions import UserError
import hashlib
from datetime import datetime
from odoo.tools import float_repr

class AccountJournal(models.Model):
    _inherit = "account.journal"
    
    jabra_qr = fields.Boolean('Hide jabra QR')


class AccountMove(models.Model):
    _inherit = "account.move"
    l10n_sa_qr_code_str = fields.Char(string='Jabra QR Code', compute='_compute_qr_code_str')
    expenses = fields.Boolean('Expenses')
    print_count=fields.Integer('Count')
    remarks=fields.Char('Remarks')
    vat_id = fields.Char(related='partner_id.vat',string='Vat',store=True,readonly=True)
    partner_balance = fields.Monetary(
        string="Balance", compute="_compute_partner_balance",currency_field="currency_id"
    )
    jabra_qr_base64 = fields.Char(string="Jabra QR (Base64)", readonly=True, copy=False)
    jabra_hash = fields.Char(string="Jabra Invoice Hash", readonly=True, copy=False)

    def get_report_head_values(self):

        for rec in self:
            # if rec.print_count > 0 and not self.env.user.has_group('zb_saudi_vat_customisations.group_duplicate_invoice'):
            #     raise ValidationError(_("Only allowed to print once"))
            # rec.print_count+=1
            # print("hhhhhhhhhHH",rec.l10n_sa_qr_code_str)
            name = "VAT INVOICE   فاتورة الضريبة القيمة المضافة "
            if rec.amount_tax == 0:
                name = "Branch Transfer"

            elif rec.move_type == "out_invoice":
                # name = "SALE INVOICE ‫فاتورة المبيعات‬"
                name="Tax Invoice  فاتورة ضريبية"
            elif rec.move_type == "out_refund":
                name = "SALES RETURN INVOICE ‫فاتورة‬ ‫مبيعات‬ ‫العودة‬"
                print(name)
            return [{'name': name}]

   
    @staticmethod
    def _tlv(tag, value):
        value = value or ""
        value_bytes = value.encode("utf-8")
        return bytes([tag, len(value_bytes)]) + value_bytes

    def _generate_local_qr(self):
    
        def get_qr_encoding(tag, value):
            value = value or ''
            value_bytes = value.encode('utf-8')
            return (
                tag.to_bytes(length=1, byteorder='big') +
                len(value_bytes).to_bytes(length=1, byteorder='big') +
                value_bytes
            )
    
        for move in self:
            if move.move_type not in ("out_invoice", "out_refund"):
                continue
            if not move.company_id.vat or not move.create_date:
                continue
    
            seller_name_enc = get_qr_encoding(
                1, move.company_id.name
            )
    
            vat_number_enc = get_qr_encoding(
                2, move.company_id.vat
            )
    
            time_sa = fields.Datetime.context_timestamp(
                move.with_context(tz='Asia/Riyadh'),
                move.create_date
            )
            timestamp_enc = get_qr_encoding(
                3, time_sa.isoformat()
            )
    
            invoice_total_enc = get_qr_encoding(
                4, float_repr(abs(move.amount_total), 2)
            )
    
            vat_amount_enc = get_qr_encoding(
                5, float_repr(abs(move.amount_tax), 2)
            )
    
            # Combine TLV bytes
            qr_bytes = (
                seller_name_enc +
                vat_number_enc +
                timestamp_enc +
                invoice_total_enc +
                vat_amount_enc
            )
    
            qr_value = base64.b64encode(qr_bytes).decode()
    
            super(type(move), move).write({
                'jabra_qr_base64': qr_value
            })

    def _generate_invoice_hash(self):
        for move in self:
            base_string = f"{move.name}|{move.amount_total}|{move.invoice_date}"
            hash_value = hashlib.sha256(base_string.encode()).hexdigest()

            super(AccountMove, move).write({
                'jabra_hash': hash_value
            })

  
    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._generate_local_qr()
        record._generate_invoice_hash()
        return record
    def write(self, vals):
        if set(vals).issubset({'jabra_qr_base64', 'jabra_hash'}):
            return super().write(vals)
    
        res = super().write(vals)
        self._generate_local_qr()
        self._generate_invoice_hash()
        return res

    def get_buyer_details_report_values(self):
        list=[]
        for rec in self:
            dict={
                
                'name':rec.partner_id.display_name or False,
                'building_number': rec.partner_id.l10n_sa_edi_building_number or False,
                'street':rec.partner_id.street or False,
                'district':rec.partner_id.street2 or False,
                'city':rec.partner_id.city or False,
                'state':rec.partner_id.state_id.name or False,
                'country':rec.partner_id.country_id.name or False,
                'vat': rec.partner_id.vat or False,
                'zip':rec.partner_id.zip or False,
                'additional':rec.partner_id.l10n_sa_edi_plot_identification or False,
                'arabic_building':rec.partner_id.arabic_building or False,
                'arabic_name':rec.partner_id.arabic_name or False,
                'arabic_street':rec.partner_id.arabic_street or False,
                'arabic_district':rec.partner_id.arabic_street2 or False,
                'arabic_city':rec.partner_id.arabic_city or False,
                'arabic_state_id':rec.partner_id.state_id.arabic_name or False,
                'arabic_vat':rec.partner_id.arabic_vat or False,
                'arabic_zip':rec.partner_id.arabic_zip or False,
                'arabic_country':rec.partner_id.country_id.arabic_name or False,
                'arabic_additional':rec.partner_id.additional_no or False,
                
                
                
                }
            list.append(dict)
            return list
        
    

    def number_to_arabic_text(self,number):
        return num2words(number, lang='ar')
    def number_to_englsih_text(self,number):
        return num2words(number, lang='en')

        
    def get_product_data_report_values(self):
        list=[]
        sl=1
        for rec in self:
            for line in rec.invoice_line_ids:
                if not line.product_id == line.company_id.sale_discount_product_id:
                    vals={
                        
                        'sl':sl,
                        'code':line.product_id.code if line.product_id.code else False,
                        'name':line.product_id.name if line.product_id.name else False,
                        'uom':line.product_uom_id.name if line.product_uom_id else False,
                        'uom_display_name': line.product_uom_id.display_name if line.product_uom_id else False,
                        'qty':line.quantity or 0,
                        'description_sale':line.product_id.description_sale or '',
                        'rate':line.price_unit or 0,
                        'gross':line.price_subtotal or 0,
                        'vat':line.tax_ids.name or False,
                        'vat_sar':round(abs(line.price_total - line.price_subtotal), 2) or 0,
                        'total':line.price_total or 0,
                        
                        'total_amt':2300,
                        'discount':10,
                        'tax_amount':2200,
                        'vat_total':5432,
                        'net_amt':1113
                        }
                    list.append(vals)
                    sl+=1
        return list
    
    
    
    def get_product_sum_report_values(self):
        net_amt=vat_total=tax_amount=discount=total_amt=0
        k={}
        for rec in self:
            rec.print_count+=1
            for line in rec.invoice_line_ids:
                if line.product_id == line.company_id.sale_discount_product_id:
                    discount = line.price_subtotal * -1
                else:
                    total_amt+=line.price_subtotal
                tax_amount+=line.price_subtotal
                vat_total=vat_total+(abs(line.price_total-line.price_subtotal))
                net_amt+=line.price_total
            arabic_amt = rec.number_to_arabic_text(round(net_amt,2))
            amt_in_words = rec.number_to_englsih_text(round(net_amt,2))
            print(amt_in_words)
            return[{'total_amt':total_amt,'discount':discount,'tax_amount':tax_amount,'vat':vat_total,'net_amt':net_amt,'amt_in_words':amt_in_words,'arabic_amt':arabic_amt}]
                
    

    @api.depends('partner_id')
    def _compute_partner_balance(self):
        """Compute partner balance across all companies using SQL for posted entries."""
        for record in self:
            record.partner_balance = 0.0  # Default
            
            if not record.partner_id:
                continue
    
            # Define filters
            state_condition = "AND am.state = 'posted'"
            account_type_condition = "AND aa.account_type IN ('asset_receivable', 'liability_payable')"
    
            # Build SQL query WITHOUT company filter
            query = f"""
                SELECT 
                    COALESCE(SUM(aml.debit), 0) - COALESCE(SUM(aml.credit), 0) AS balance
                FROM account_move_line aml
                JOIN account_account aa ON aml.account_id = aa.id
                JOIN account_move am ON aml.move_id = am.id
                WHERE aml.partner_id = %s
                {state_condition}
                {account_type_condition}
            """
    
            params = (record.partner_id.id,)
            self.env.cr.execute(query, params)
            result = self.env.cr.fetchone()
    
            record.partner_balance = result[0] if result else 0.0


        
        