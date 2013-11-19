import sys
sys.path.insert(0, 'lib')

from google.appengine.ext.webapp.util import run_wsgi_app
from knowyourgov import app

run_wsgi_app(app)
