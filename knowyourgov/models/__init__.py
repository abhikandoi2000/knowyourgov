from google.appengine.ext import db

class User(db.Model):
  name = db.StringProperty(required = True)
  username = db.StringProperty(required = True)
  email = db.StringProperty(default = '')
  created = db.DateTimeProperty(auto_now_add = True)
  updated = db.DateTimeProperty(auto_now = True)