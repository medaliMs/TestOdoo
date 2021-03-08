# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import datetime
from . import tuleap_data


class UserStory(models.Model):
    _inherit = "account.analytic.line"
    user_story_id = fields.Char(string='User Story')

    @api.model
    def add(self):
        file = open("/odoo/odoo-server/my_addons/vente/models/sync-date.txt", "r+")
        date_sync = file.read()
        print(date_sync)
        file.close()
        # print(tuleap_data.get_Data())
        items_to_create = []
        items_from_script = tuleap_data.get_Data()
        # items_from_script = [{'userstory_id': '295735', 'userstory_title': 'Gestion utilisateurs', 'project_id': '4571',
        #                       'project_name': 'SNCF Courrier', 'user_id': 3571, 'time_spent': 2},
        #                      {'userstory_id': '295736', 'userstory_title': 'Gestion utilisateurs', 'project_id': '123',
        #                       'project_name': 'SNCF Courrier', 'user_id': 145, 'time_spent': 1}]
        print(self)
        bool = True
        for item in items_from_script:
            item_to_search = self.search([('user_story_id', '=', item['userstory_id'])])
            print(item_to_search)
            if item_to_search:
                print("item found")
                project = self.env['project.project'].search([('alm_project_id', '=', item['project_id'])])
                employee = self.env['hr.employee'].search([('alm_user_id', '=', item['user_id'])])
                print(project)
                print(employee)
                if not employee:
                    print("employee not found please create it first")
                    bool = False
                    continue

                elif not project:
                    print("project not found please create it first")
                    bool = False
                    continue
                # task_to_insert = {'id': None, 'name': item['userstory_id'], 'project_id': project.id}
                item_to_update = {'date': datetime.today().strftime('%Y-%m-%d'), 'user_story_id': item['userstory_id'],
                                  'employee_id': employee.id, 'project_id': project.id, 'task_id': False,
                                  'name': item['userstory_title'], 'unit_amount': item['time_spent'], 'user_id': False}
                print(item_to_update)
                item_to_search.write(item_to_update)
            else:
                print('item not found')
                project = self.env['project.project'].search([('alm_project_id', '=', item['project_id'])])
                employee = self.env['hr.employee'].search([('alm_user_id', '=', item['user_id'])])
                print(project)
                print(employee)
                if not employee:
                    print("employee not found please create it first")
                    bool = False
                    continue
                elif not project:
                    print("project not found please create it first")
                    bool = False
                    continue
                item_to_insert = {'date': datetime.today().strftime('%Y-%m-%d'), 'user_story_id': item['userstory_id'],
                                  'employee_id': employee.id, 'project_id': project.id, 'task_id': False,
                                  'name': item['userstory_title'], 'unit_amount': item['time_spent'], 'user_id': False}

                items_to_create.append(item_to_insert)
        if items_to_create:
            self.create(items_to_create)
        if bool:
            print("sync successful")
            file = open("/odoo/odoo-server/my_addons/vente/models/sync-date.txt", "w+")
            file.truncate()
            file.write(str(datetime.today()))
            file.close()
        else:
            print("sync not successful")


class AlmProject(models.Model):
    _inherit = "project.project"
    alm_project_id = fields.Char(string='Alm Project')


class AlmUser(models.Model):
    _inherit = "hr.employee"
    alm_user_id = fields.Char(string='Alm User')
