import math
import re


from odoo import models, fields, api, exceptions


class MadfoxPurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'
    retained_percentage = fields.Float(string="retain percentage")
    payment_term_id = fields.Many2one(comodel_name='account.payment.term', string="Payment Terms")
    
    def action_in_progress(self):
        lines = []
        res = super(MadfoxPurchaseRequisition, self).action_in_progress()
        #calc Purchase Requisition total amount
        totalAmount = 0
        total=0
        for line in self.line_ids:
            totalAmount += line.product_qty * line.price_unit
        # get the tax rules
        taxRules = self.env['account.tax'].search([('id', '=', 11)])
        stampValue = 0
        taxs = []
        i = 1
        account = self.env['account.account'].search([('code', '=', '335030')])
        if(taxRules.children_tax_ids):
            for taxRule in taxRules.children_tax_ids:
                if(i==1):
                    #the stamp rules
                    stampValue=(taxRule.amount /100) * totalAmount
                    total=stampValue
                    taxs.append([stampValue,taxRule.name])
                    lines.append([0, False, {'account_id': account.id,  'name': taxRule.name,
                         'debit': 0, 'credit': stampValue, 'partner_id': 21,}])
                else:
                    taxs.append([(taxRule.amount / 100) * stampValue,taxRule.name])
                    total= total+ ((taxRule.amount / 100) * stampValue)
                    lines.append([0, False, {'account_id': account.id, 'name': taxRule.name,
                                             'debit': 0, 'credit':(taxRule.amount / 100) * stampValue, 'partner_id': 21,}])

                i = i + 1
                    #create account move entre
        lines.append([0, False, {'account_id': account.id, 'name': 'مدفوعات',
									 'debit': total, 'credit':0, 'partner_id': 21,}])
        self.env['account.move'].create({
             'name': 'purchase agreement taxes',   'ref': 'purchase agreement' ,'requisition_id': self.id,
            'journal_id': 3, 'line_ids': lines
        })
        return res
