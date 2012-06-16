#!/usr/bin/env python
import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import models
import markdown
import settings

_DEBUG = True

class MockRequest(object):
    def __init__(self):
        self.uri = 'http://localhost:8080'
        self.host = 'localhost:8080'

class BaseRequestHandler(webapp.RequestHandler):
    """Supplies a common template generation function.

    When you call renderTemplate(), we augment the template variables supplied with
    the current user in the 'user' variable and the current webapp request
    in the 'request' variable.
    """
    def renderTemplate(self, template_name, template_values={}):
        req = self.request if hasattr(self, 'request') else MockRequest()
        values = {
            'request': req,
            'user': users.get_current_user(),
            'is_admin': users.is_current_user_admin(),
            'login_url': users.create_login_url(req.uri),
            'logout_url': users.create_logout_url('http://%s%s' % (req.host, settings.URLS['index'])),
            'URLS': settings.URLS,
            }
        values.update(template_values)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, os.path.join('templates', template_name))
        return template.render(path, values, debug=_DEBUG)

    def get(self):
        self.response.out.write(self.render())

class IndexHandler(BaseRequestHandler):
    def render(self):
        entries = []
        for entry in models.BlogEntry.all().order('-created'):
            entry.text = markdown.markdown(entry.text)
            entries.append(entry)
        return self.renderTemplate('index.html', {
            'entries': entries
            })

class NewBlogEntryHandler(BaseRequestHandler):
    def post(self):
        title = self.request.POST.get('title')
        text = self.request.POST.get('text')
        models.BlogEntry(title = title, text = text).save()
        self.redirect(settings.URLS['index'])

    def render(self):
        return self.renderTemplate('new-blog-entry.html')

class EditBlogEntryHandler(BaseRequestHandler):
    def post(self):
        id = self.request.POST.get('id')
        entry = models.BlogEntry.get_by_id(int(id))
        title = self.request.POST.get('title')
        text = self.request.POST.get('text')
        entry.title = title
        entry.text = text
        entry.save()
        self.redirect(settings.URLS['index'])

    def render(self):
        id = self.request.GET.get('id')
        entry = models.BlogEntry.get_by_id(int(id))
        return self.renderTemplate('edit-blog-entry.html', {
            'entry': entry
            })

class XsrfTokenHandler(BaseRequestHandler):
    def render(self):
        if not self.request.host.startswith('localhost:'):
            return 'access from %s' % self.request.host
        from google.appengine.ext import admin
        return admin.get_xsrf_token()

app = webapp.WSGIApplication([
        (settings.BASE + '/', IndexHandler),
        (settings.BASE + '/new', NewBlogEntryHandler),
        (settings.BASE + '/edit', EditBlogEntryHandler),
        (settings.BASE + '/xsrf_token', XsrfTokenHandler),
        ],
        debug=True)
