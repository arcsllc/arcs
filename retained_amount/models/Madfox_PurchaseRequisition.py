import math
import re

from odoo import models, fields, api, exceptions


class MadfoxPurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'
    retained_percentage = fields.Float(string="retain percentage")
    payment_term_id = fields.Many2one(comodel_name='account.payment.term', string="Payment Terms")
    name = fields.Char(string='Reference', required=True, copy=False, default='New', readonly=False)

    def action_in_progress(self):
        lines = []
        res = super(MadfoxPurchaseRequisition, self).action_in_progress()
        # calc Purchase Requisition total amount
        totalAmount = 0
        total = 0
        for line in self.line_ids:
            totalAmount += line.product_qty * line.price_unit
        # get the tax rules
        taxRules = self.env['account.tax'].search([('id', '=', 11)])
        stampValue = 0
        taxs = []
        i = 1
        account = self.env['account.account'].search([('code', '=', '230703')])
        if (taxRules.children_tax_ids):
            for taxRule in taxRules.children_tax_ids:
                if (i == 1):
                    # the stamp rules
                    stampValue = (taxRule.amount / 100) * totalAmount
                    total = stampValue
                    taxs.append([stampValue, taxRule.name])
                    lines.append([0, False, {'account_id': account.id, 'name': taxRule.name,
                                             'credit': 0, 'debit': stampValue, 'partner_id': 21, }])
                elif i == 2:
                    taxs.append([(taxRule.amount / 100) * stampValue, taxRule.name])
                    total = total + ((taxRule.amount / 100) * stampValue)
                    account = self.env['account.account'].search([('code', '=', '230704')])
                lines.append([0, False, {'account_id': account.id, 'name': taxRule.name,
                                         'credit': 0, 'debit': (taxRule.amount / 100) * stampValue,
                                         'partner_id': 21, }])

            else:
                taxs.append([(taxRule.amount / 100) * stampValue, taxRule.name])
                total = total + ((taxRule.amount / 100) * stampValue)
                account = self.env['account.account'].search([('code', '=', '230705')])
            lines.append([0, False, {'account_id': account.id, 'name': taxRule.name,
                                     'credit': 0, 'debit': (taxRule.amount / 100) * stampValue, 'partner_id': 21, }])

        i = i + 1
        # create account move entre

        account = self.env['account.account'].search([('code', '=', '335030')])
        lines.append([0, False, {'name': 'ضريبة عقد'+' ('+res.user_id.display_name+' '+res.name+')',
                         'debit': 0, 'credit': total, 'partner_id': 1, 'account_id': account.id}])
        self.env['account.move'].create({
        'name': 'purchase agreement taxes', 'ref': 'purchase agreement', 'requisition_id': self.id,
        'journal_id': 3, 'line_ids': lines
        })
        return res
