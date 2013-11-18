from flask import Flask, url_for, render_template, request, make_response

from knowyourgov import app
from knowyourgov.models import Politician
from knowyourgov.scripts import insert_politicians_in_db
# import errors

# landing page
"""Home page
"""
@app.route('/')
def homepage():
  return render_template('home.html')

"""Search -> Politician Page
"""
@app.route('/search', methods= ['POST', 'GET'] )
def search():
 # query = request.form['q']
  query = request.args.get('q')
  return render_template('politican.html', q = query)


""" 404 - Page
"""
@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html'), 404

""" 500 - Page
"""
@app.errorhandler(500)
def page_not_found(error):
	return render_template('500.html'), 500

"""JSON response containing information for a particular politician
"""
@app.route('/politicians/<politician>')
def display_politician(politician):
  return '{"message":"success"}';


"""Creates entry for loksabha politicians in the db
    *Note* : Do not run it more than once, will create multiple entries
"""
@app.route('/politicians/update')
def update_all():
  return insert_politicians_in_db()
