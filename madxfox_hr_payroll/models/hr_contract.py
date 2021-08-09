
from odoo import api, fields, models, _

class MadFox_HrContract(models.Model):
    _inherit = 'hr.contract'

    representation_compensation = fields.Monetary(string='Representation Compensation')
    responsibility_compensation = fields.Monetary(string='Responsibility Compensation')
    work_conditions_compensation = fields.Monetary(string='Work Conditions Compensation')
    transportation_compensation = fields.Monetary(string='Transportation Compensation')
    inflation_compensation = fields.Monetary(string='Inflation Compensation')
    


    @api.model
    def create(self, vals):
        contract = super(MadFox_HrContract, self).create(vals)
        #need to set the other inputs
        return contract
