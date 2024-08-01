# -*- coding: utf-8 -*-
# from odoo import http


# class Teachers(http.Controller):
#     @http.route('/teachers/teachers', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/teachers/teachers/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('teachers.listing', {
#             'root': '/teachers/teachers',
#             'objects': http.request.env['teachers.teachers'].search([]),
#         })

#     @http.route('/teachers/teachers/objects/<model("teachers.teachers"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('teachers.object', {
#             'object': obj
#         })

