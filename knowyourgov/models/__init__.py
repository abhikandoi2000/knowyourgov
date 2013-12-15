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
  state = db.StringProperty()
  constituency = db.StringProperty()
  position = db.StringProperty()
  wiki_link = db.StringProperty(required = True)
  search_count = db.IntegerProperty(default = 0)
  image_url = db.StringProperty()
  dob = db.StringProperty()
  gender = db.IntegerProperty(default = 0)
  # gender: 0 - not known, 1 - male, 2 - female
  membership = db.StringProperty()
  startofterm = db.StringProperty()
  endofterm = db.StringProperty()
  education = db.StringProperty()
  debates = db.IntegerProperty(default= 0)
  bills = db.IntegerProperty(default= 0)
  questions = db.IntegerProperty(default= 0)
  attendance = db.IntegerProperty(default= 0)

  def url_slug(self):
    return self.name.replace(' ','-').lower()
  def gender_str(self):
    if self.gender == 1:
      return "Male"
    elif self.gender == 2:
      return "Female"
    else:
      return "None"
