# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Command(http.Controller):
    @http.route('/vente/command/', auth='public', website=True)
    def index(self, **kw):
        # return "Hello, world"
        commands = request.env['vente.command'].sudo().search([])
        return request.render("vente.commands_page", {
            'commands': commands
        })

    @http.route('/bb', auth='public', website=True)
    def index2(self, **kw):
        return "Hello, world"

    @http.route('/test', auth='public', website=True)
    def index3(self, **kw):
        value = {'value': 1}
        return request.render("vente.test_owl", value)

    @http.route(['/vente/command/details/<model("vente.command"):command>'], type='http', auth='public', website=True)
    def article(self, command):
        values = {'command': command}
        return request.render("vente.command_details", values)


class Article(http.Controller):
    @http.route('/vente/article/', auth='public', website=True)
    def index(self, **kw):
        # return "Hello, world"
        articles = request.env['vente.article'].sudo().search([])
        return request.render("vente.articles_page", {
            'articles': articles
        })

    @http.route('/article_form', type="http", auth="public", website=True)
    def article_form(self,**kw):
        return http.request.render('vente.article_form', {})

    # @http.route('/article_delete', type="http", auth="public", website=True)
    # def article_form(self,**kw):
    #     article = request.env['vente.article'].sudo().search(kw)
    #     request.env['vente.article'].sudo().unlink(article)
    #     return http.request.render('vente.article_form', {})

    @http.route('/create/article', type="http", auth="public", website=True)
    def create_article(self,**kw):
        request.env['vente.article'].sudo().create(kw)
        return request.render("vente.article_done",{})

    @http.route(['/vente/article/details/<model("vente.article"):article>'], type='http', auth='public', website=True)
    def article(self, article):
        values = {'article': article}
        return request.render("vente.article_details", values)

    @http.route(['/vente/article/delete/<model("vente.article"):article>'], type='http', auth='public', website=True)
    def delete_article(self, article):
        # request.env['vente.article'].sudo().unlink()
        article.unlink()
        # values = {'article': article}
        # return request.render("vente.article_details", values)
        return request.redirect('/vente/article')

    @http.route(['/vente/article/edit/<model("vente.article"):article>'], type='http', auth='public', website=True)
    def edit_article(self, article):
        # request.env['vente.article'].sudo().unlink()
        # article.unlink()
        values = {'article': article}
        return request.render("vente.article_edit", values)
        # return request.redirect('/vente/article')

    @http.route('/edit/article/', type="http", auth="public", website=True)
    def update_article(self, **kw):
        print('kw = ', kw)
        article = request.env['vente.article'].sudo().browse(kw['id'])
        # article = request.env['vente.article'].sudo().search(['id', '=', kw['id']])
        print('article=  ',article,'of type  =   ',type(article))

        value={'name': kw['name'], 'price': kw['price']}
        # print('value = ',value)
        article.write(value)
        return request.redirect('/')


class Client(http.Controller):
    @http.route('/vente/client/', auth='public', website=True)
    def index(self, **kw):
        # return "Hello, world"
        clients = request.env['vente.client'].sudo().search([])
        return request.render("vente.clients_page", {
            'clients': clients
        })

    @http.route(['/vente/client/details/<model("vente.client"):client>'], type='http', auth='public', website=True)
    def article(self, client):
        values = {'client': client}
        return request.render("vente.client_details", values)

#     @http.route('/module/module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('module.listing', {
#             'root': '/module/module',
#             'objects': http.request.env['module.module'].search([]),
#         })

#     @http.route('/module/module/objects/<model("module.module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('module.object', {
#             'object': obj
#         })
