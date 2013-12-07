from google.appengine.ext import db

class User(db.Model):
  name = db.StringProperty(required = True)
  username = db.StringProperty(required = True)
  email = db.StringProperty(default = '')
  created = db.DateTimeProperty(auto_now_add = True)
  updated = db.DateTimeProperty(auto_now = True)

class Politician(db.Model):
  name = db.StringProperty(required = True)
  party = db.StringProperty(required = True)
  constituency = db.StringProperty()
  state = db.StringProperty()
  wiki_link = db.StringProperty(required = True)
  search_count = db.IntegerProperty(default = 0)
  image_url = db.StringProperty()
  dob = db.StringProperty()
  gender = db.IntegerProperty(default= 1) #True=1=Male
  def url_slug(self):
    return self.name.replace(' ','-').lower()