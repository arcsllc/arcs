# -*- coding: utf-8 -*-
# from odoo import http


# class RetainedAmount(http.Controller):
#     @http.route('/retained_amount/retained_amount/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/retained_amount/retained_amount/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('retained_amount.listing', {
#             'root': '/retained_amount/retained_amount',
#             'objects': http.request.env['retained_amount.retained_amount'].search([]),
#         })

#     @http.route('/retained_amount/retained_amount/objects/<model("retained_amount.retained_amount"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('retained_amount.object', {
#             'object': obj
#         })
