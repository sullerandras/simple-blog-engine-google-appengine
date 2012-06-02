#!/usr/bin/env python
import os
from google.appengine.dist import use_library

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
use_library('django', '1.2')
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

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
        'logout_url': users.create_logout_url('http://%s/' % (req.host,))
        }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    return template.render(path, values, debug=_DEBUG)

class IndexHandler(BaseRequestHandler):
    def get(self):
        self.response.out.write(self.render())

    def render(self):
        return self.renderTemplate('index.html')

class NewBlogEntryHandler(BaseRequestHandler):
    def get(self):
        self.response.out.write(self.render())

    def render(self):
        return self.renderTemplate('new-blog-entry.html')

app = webapp.WSGIApplication([('/', IndexHandler), ('/new', NewBlogEntryHandler)],
                              debug=True)
