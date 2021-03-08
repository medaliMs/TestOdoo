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
        print(tuleap_data.get_Data())
        items_to_create = []

        # item_from_script = tuleap_data.get_Data()
        items_from_script = [{'userstory_id': '295735', 'userstory_title': 'Gestion utilisateurs', 'project_id': '4571',
                              'project_name': 'SNCF Courrier', 'user_id': 3571, 'time_spent': 2},
                             {'userstory_id': '295736', 'userstory_title': 'Gestion utilisateurs', 'project_id': '4571',
                              'project_name': 'SNCF Courrier', 'user_id': 3570, 'time_spent': 1}]
        print(self)
        for item in items_from_script:
            item_to_search = self.search([('user_story_id', '=', item['userstory_id'])])
            print(item_to_search)
            if item_to_search:
                print("item found")

                # print(item.employee_id , "of type :" , type(item.employee_id))
                # print(item.employee_id.alm_user_id)
                # print(item.project_id , "of type :" , type(item.project_id))
                # print(item.project_id.alm_project_id)
                project = self.env['project.project'].search([('alm_project_id', '=', item['project_id'])])
                employee = self.env['hr.employee'].search([('alm_user_id', '=', item['user_id'])])
                print(project)
                print(employee)
                if not employee:
                    # raise ValidationError("employee not found please create it first")
                    print("employee not found")
                    continue

                elif not project:
                    # raise ValidationError("project not found please create it first")
                    print("project not found")
                    continue

                item_to_update = {'date': datetime.today().strftime('%Y-%m-%d'), 'user_story_id': item['userstory_id'],
                                  'employee_id': employee.id, 'project_id': project.id, 'task_id': False,
                                  'name': item['userstory_title'], 'unit_amount': item['time_spent'], 'user_id': False}
                print(item_to_update)
                item.write(item_to_update)
            else:
                project = self.env['project.project'].search([('alm_project_id', '=', item['project_id'])])
                employee = self.env['hr.employee'].search([('alm_user_id', '=', item['user_id'])])
                print(project)
                print(employee)
                if not employee:
                    # raise ValidationError("employee not found please create it first")
                    print("employee not found")
                    continue
                elif not project:
                    # raise ValidationError("project not found please create it first")
                    print("project not found")
                    continue
                item_to_insert = {'date': datetime.today().strftime('%Y-%m-%d'), 'user_story_id': item['userstory_id'],
                                  'employee_id': employee.id, 'project_id': project.id, 'task_id': False,
                                  'name': item['userstory_title'], 'unit_amount': item['time_spent'], 'user_id': False}
                # item_to_insert_or_update[0]["date"] = '2021-05-13'
                # item_to_insert_or_update[0]["user_story_id"] = item['userstory_id']
                # item_to_insert_or_update[0]["employee_id"] = employee.id
                # item_to_insert_or_update[0]["project_id"] = project.id
                # item_to_insert_or_update[0]["name"] = item['userstory_title']
                # item_to_insert_or_update[0]["unit_amount"] = item['time_spent']
                # print(item_to_insert_or_update[0])

                # item_to_insert["date"] = '2021-05-13'
                # item_to_insert["user_story_id"] = item['userstory_id']
                # item_to_insert["employee_id"] = employee.id
                # item_to_insert["project_id"] = project.id
                # item_to_insert["name"] = item['userstory_title']
                # item_to_insert["unit_amount"] = item['time_spent']
                # print(item_to_insert)
                items_to_create.append(item_to_insert)

        self.create(item_to_insert_or_update)


class AlmProject(models.Model):
    _inherit = "project.project"
    alm_project_id = fields.Char(string='Alm Project')


class AlmUser(models.Model):
    _inherit = "hr.employee"
    alm_user_id = fields.Char(string='Alm User')
