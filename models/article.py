# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Article(models.Model):
    _name = 'vente.article'
    _description = 'vente.module'

    name = fields.Char(string='Name', required=True)
    price = fields.Integer(string='Price', required=True)
    stock = fields.Boolean(string='Stock', required=True)
    description = fields.Text(string='Description')
    command_ids = fields.Many2many(comodel_name='vente.command', relation='table_name', column1='name', column2='code',
                                   readonly=True)

    @api.constrains('price')
    def _check_value(self):
        if not(0 < self.price):
            raise ValidationError('price must be a positive number')

    @api.onchange('stock')
    def check_change(self):

        if not self.stock:
            for item in self.command_ids:

                item.state = 'cancel'

        # else:
        #             item.state = 'confirmed'
