import math
import re


from odoo import models, fields, api, exceptions
# from openerp.addons.retained_amount import models


class Madfox_AccountMove(models.Model):
    _inherit = 'account.move'
    requisition_id = fields.Char(name='req id')


    @api.model
    def create(self, vals):
       
        res = super(Madfox_AccountMove, self).create(vals)
        if res.move_type=='in_invoice' and res.invoice_line_ids.purchase_order_id and res.invoice_line_ids.purchase_order_id.requisition_id.retained_percentage>0:
            retained_amount=0
            percentage=(res.invoice_line_ids.purchase_order_id.requisition_id.retained_percentage/100)
            for line in res.invoice_line_ids:
                retained_amount = retained_amount+retained_amount+( lines.price_subtotal * percentage)
            account = self.env['account.account'].search([('code', '=', '230101')])
            if account:
                rec = {
                    'partner_id': res.partner_id,
                    'quantity': '1',
                    'name': 'Retained Amount',
                    'price_unit': retained_amount*-1,
                    'account_id': account.id
                }
            else:
                rec = {
                    'partner_id': res.partner_id,
                    'quantity': '1',
                    'name': 'Retained Amount',
                    'price_unit': retained_amount * -1,

                }
            res.invoice_line_ids=[(0,0,rec)]

        return res




