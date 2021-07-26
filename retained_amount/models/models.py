# -*- coding: utf-8 -*-

from odoo import models, fields, api


class retained_amount(models.Model):
    _name = 'retained_amount'
#     _description = 'retained_amount.retained_amount'

    # name = fields.Char()
    name = fields.Char('Name', index=True, required=True)
    partner_id = fields.Many2one('res.partner')
    contract_id = fields.Many2one('purchase.order')
    bill_id = fields.Many2one('account.move')
    amount = fields.Float('Amount')
    retained_percentage = fields.Float('Retained Percentage')
    retained_amount = fields.Float('Retained Amount')
    is_paid = fields.Boolean('Is Paid')
    date = fields.Date('Pay Date')


#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
