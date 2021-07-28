# -*- coding: utf-8 -*-

from odoo import models, fields, api


class retained_amount(models.Model):
    _name = 'retained'

    partner_id = fields.Float('Company')
    original_amount = fields.Float('Amount')
    retained_percentage = fields.Float('Retained Percentage')
    retained_amount = fields.Float('Retained Amount')
    agreement_id = fields.Float('purchase agreement')
