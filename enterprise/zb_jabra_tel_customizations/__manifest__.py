# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2026 ZestyBeanz Technologies(<http://www.zbeanztech.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Jabra Tel Customizations",
    "version": "19.0.1.0.0",
    "category": "Accounting",
    'author': 'ZestyBeanz Technologies',
    "website": "www.zbeanztech.com",
    'license': "LGPL-3",
    "summary": "Custom Simplified Tax Invoice for Jabra Tel",
    "depends": ["base","account"],
    "data": [
        "views/account_move.xml",
        # "views/res_company_views.xml",
        "report/invoice_report.xml",
        "report/invoice_templates.xml",
        "report/sale_report_invoice.xml",

    ],
    "installable": True,
    "application": False,
}