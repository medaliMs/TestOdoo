# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    client_name = fields.Char(string='client name')


# class Timesheet(models.Model):
#     _inherit = "account.analytic.line"
#


class Client(models.Model):
    _name = 'vente.client'
    _description = 'vente.client'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)

    age = fields.Integer(string='Age')
    command_ids = fields.One2many(comodel_name='vente.command', inverse_name='client_id')

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail!')

    @api.constrains('age')
    def _check_value(self):
        if not (18 < self.age <= 90):
            raise ValidationError('incorrect age')

    def unlink(self):
        if len(self.command_ids) != 0:
            raise ValidationError('user with commands cannot be deleted. delete your command first')
        return super(Client, self).unlink()

    @api.model
    def first_cron(self):
        client = {'name': 'name', 'age': 40, 'email': 'aa@bb.com'}
        items = self.search([])
        for item in items:
            for command in item.command_ids:
                print(command.code)
        client_search = self.browse(['name', '=', 'client1'])
        print(client_search)
        if not client_search:
            self.create(client)
        test = [
            {'date': '2021-03-05', 'employee_id': 1, 'project_id': 6, 'task_id': False, 'name': False, 'unit_amount': 0,
             'user_id': 2}]
        print(type(test))
        # [{'date': '2021-03-05', 'employee_id': 1, 'project_id': 6, 'task_id': False, 'name': False, 'unit_amount': 0,
        #   'user_id': 2}]

