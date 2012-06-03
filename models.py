from google.appengine.ext import db

class BlogEntry(db.Model):
  """Represents a blog entry."""
  title = db.StringProperty(required = True)
  text = db.StringProperty(required = True, multiline = True)
  created = db.DateTimeProperty(auto_now_add = True)
