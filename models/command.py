# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import _


class Command(models.Model):
    _name = 'vente.command'
    _description = 'vente.command'
    code = fields.Char(string='Code')
    totale = fields.Integer(string='Totale', readonly=True, compute='sum_totale')
    state = fields.Selection([
        ('confirmed', 'confirmed'),
        ('progress', 'in progress'),
        ('done', 'done'),
        ('cancel', 'canceled')

    ], default='confirmed')
    client_id = fields.Many2one(comodel_name='vente.client')
    article_ids = fields.Many2many(comodel_name='vente.article', relation='table_name', column1='code', column2='name')

    def sum_totale(self):
        sum = 0
        for item in self.article_ids:
            sum += item.price
        self.totale = sum

    @api.onchange('article_ids')
    def check_change(self):
        for item in self.article_ids:
            if not item.stock:
                self.state = 'cancel'
                break
            else:
                self.state = 'confirmed'

    def unlink(self):
        for command in self:
            if command.state in ['done', 'progress']:
                raise UserError("too late to delete")
        return super(Command, self).unlink()

    def name_get(self):
        result = []
        for item in self:
            name = '['+item.client_id.name+'] '+item.code
            result.append((item.id, name))
        return result

    def next_level(self):
        if self.state == 'confirmed':
            self.state = 'progress'
        elif self.state == 'progress':
            self.state = 'done'
        elif self.state == 'done':
            raise UserError('command is done')

    # def write(self, vals):
    #     if any(state == 'done' for state in set(self.mapped('state'))):
    #         raise UserError(_("No edit in done state"))
    #     else:
    #         return super().write(vals)
