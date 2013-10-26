from flask import Flask, url_for, render_template, request, make_response

from knowyourgov import app
# import errors

# test route
@app.route('/hello')
def hello_world():
  return 'Hello!'