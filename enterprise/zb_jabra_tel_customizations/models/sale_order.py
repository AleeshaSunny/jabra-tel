from odoo import models, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for order in self:
            for line in order.order_line:

                product_price = line.product_id.list_price
                entered_price = line.price_unit

                if entered_price != product_price and not self.env.user.has_group('base.group_system'):
                    raise ValidationError(
                        _("You cannot change the product Unit Price. Only Administrator can modify it.")
                    )

        return super().action_confirm()