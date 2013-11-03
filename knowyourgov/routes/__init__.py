from flask import Flask, url_for, render_template, request, make_response

from knowyourgov import app
from knowyourgov.models import Politician
from knowyourgov.scripts import update_politicians
# import errors

# test route
@app.route('/')
def hello_world():
  return render_template('home.html')

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
  update_politicians()
  return 'Done'