import math
import re

from odoo import models, fields, api, exceptions


class MadfoxPurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'
    retained_percentage = fields.Float(string="retain percentage")
    payment_term_id = fields.Many2one(comodel_name='account.payment.term', string="Payment Terms")
    name = fields.Char(string='Reference', required=True, copy=False, default='New', readonly=False)
    total_retained_amount = fields.Integer(compute='_compute_retained_amount', string='Number of Orders')

    @api.depends('purchase_ids')
    def _compute_retained_amount(self):
        for requisition in self:
            requisition.total_retained_amount = requisition.compute_total_retained_amount()

    @api.model
    def compute_total_retained_amount(self):
        total = 0
        for po in self.purchase_ids:
            for invoice in po.invoice_ids:
                if invoice.state == 'posted':
                    for line in invoice.invoice_line_ids:
                        if line.account_id and line.account_id.code == '230101':
                            total += line.price_unit
        return total

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

                    taxs.append([stampValue, taxRule.name])
                    lines.append([0, False, {'account_id': account.id, 'name': taxRule.name,
                                             'credit': 0, 'debit': taxs[0][0], 'partner_id': 21, 'quantity':2}])
                elif i == 2:
                    taxs.append([(taxRule.amount / 100) * stampValue, taxRule.name])

                    account = self.env['account.account'].search([('code', '=', '230704')])
                    lines.append([0, False, {'account_id': account.id, 'name': taxRule.name,
                                             'credit': 0, 'debit': taxs[1][0],
                                             'partner_id': 21, 'quantity':2}])

                else:
                    taxs.append([(taxRule.amount / 100) * stampValue, taxRule.name])

                    account = self.env['account.account'].search([('code', '=', '230705')])
                    lines.append([0, False, {'account_id': account.id, 'name': taxRule.name,
                                             'credit': 0, 'debit': taxs[2][0], 'partner_id': 21, 'quantity':2}])

                i = i + 1
        # create account move entre

        account = self.env['account.account'].search([('code', '=', '335030')])
        # raise exceptions.ValidationError('total='+str(total)+', stamp='+str(stampValue)+', tax1='+str(taxs[1][0])+', tax2='+str(taxs[2][0])+', taxtotal='+str((stampValue+taxs[1][0]+taxs[2][0])))
        lines.append([0, False, {'name': 'ضريبة عقد' + ' (' + self.user_id.display_name + ' ' + self.name + ')',
                                 'debit': 0, 'credit': (taxs[0][0] + taxs[1][0] + taxs[2][0]), 'partner_id': 1,
                                 'account_id': account.id, 'quantity':2}])
        self.env['account.move'].create({
            'name': 'purchase agreement taxes', 'ref': 'purchase agreement', 'requisition_id': self.id,
            'journal_id': 3, 'line_ids': lines
        })

        return res