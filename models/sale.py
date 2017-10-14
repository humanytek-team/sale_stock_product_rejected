# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Manuel Márquez <manuel@humanytek.com>
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
###############################################################################

from datetime import datetime

from openerp import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _create_product_negation(self, product_qty):
        """Record a negation for product of line of sale order"""

        ProductRejected = self.env['product.rejected']
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        partner_id = self.order_id.partner_id.id \
            if self.order_id.partner_id \
            else False
        ProductRejected.create({
            'product_tmpl_id': self.product_id.product_tmpl_id.id,
            'product_id': self.product_id.id,
            'partner_id': partner_id,
            'qty': product_qty,
            'date': date_now,
            'company_id': self.env.user.company_id.id,
            })

    @api.onchange('product_uom_qty', 'product_uom', 'route_id')
    def _onchange_product_id_check_stock(self):

        if self.product_id.type == 'product':
            product_qty = self.env['product.uom']._compute_qty_obj(
                self.product_uom,
                self.product_uom_qty,
                self.product_id.uom_id)

            if product_qty > (self.product_id.qty_available -
                    self.product_id.outgoing_qty):

                if self.order_id.partner_id:

                    limit_hours = self.env.user.company_id.product_rejected_limit_hours
                    if limit_hours > 0:

                        ProductRejected = self.env['product.rejected']
                        last_product_negation = ProductRejected.search([
                            ('product_id', '=', self.product_id.id),
                            ('partner_id', '=', self.order_id.partner_id.id),
                            ('company_id', '=', self.env.user.company_id.id),
                            ], order='date')
                        if last_product_negation:

                            last_product_negation_date = last_product_negation[-1].date
                            last_product_negation_datetime = datetime.strptime(
                                last_product_negation_date, '%Y-%m-%d %H:%M:%S')
                            now = datetime.now()
                            diff = now - last_product_negation_datetime
                            hours_diff = (diff.seconds / 60.0) / 60
                            if hours_diff > limit_hours:
                                self._create_product_negation(product_qty)

                        else:
                            self._create_product_negation(product_qty)

                    else:
                        self._create_product_negation(product_qty)

                else:
                    self._create_product_negation(product_qty)
