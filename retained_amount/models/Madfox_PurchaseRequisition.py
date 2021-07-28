import math
import re


from odoo import models, fields, api, exceptions


class MadfoxPurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'
    retained_percentage = fields.Float(string="retain percentage", required=False)
    payment_term_id = fields.Many2one(comodel_name='account.payment.term', string="Payment Terms")
    
    def _action_confirm(self):
       res = super(MadfoxPurchaseRequisition, self)._action_confirm()
       #calc Purchase Requisition total amount
       totalAmount=0
       for line in res.line_ids:
       totalAmount+= line.qty_ordered* line.unit_price
       #get the tax rules
       taxRules=self.env['account.tax'].search([('id', '=', 11)])
       stampValue=0
       taxs=[]
       
       i=1
       if(taxRules.children_tax_ids):
        for taxRule in taxRules.children_tax_ids:
            if(i==1):
                #the stamp rules
                stampValue=(taxRule.amount /100) * totalAmount
                taxs[]=[stampValue,taxRule.name]
            else:
                taxs[]=[(taxRule.amount /100) * stampValue,taxRule.name]
            i++
        #create account move entre
       
       return res
       
       
       
