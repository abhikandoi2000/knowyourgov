from flask import Flask, url_for, render_template, request, make_response, jsonify, json

from knowyourgov import app
from knowyourgov.models import Politician
from knowyourgov.scripts import insert_politicians_in_db
from knowyourgov.scripts.scraping import scrapers
# import errors

# landing page
"""Home page
"""
@app.route('/')
def homepage():
  return render_template('home.html')

"""Politician Page
"""
@app.route('/politicians/id/<name>')
def politician_page(name):
  name = name.lower()
  politicians = Politician.all()
  politicians.filter("name =", name)
  politician = None
  for p in politicians:
    politician = p
  return render_template('politician.html', name = name, politician = politician)


"""Location Based Search
"""
@app.route('/locate', methods= ['POST' ,'GET'] )
def locate():
  query = request.args.get('q').lower()
  politicians = Politician.all()
  politicians.filter("state =", query)
  return render_template('locate.html', politicians=politicians, state=query)


"""Search -> Politician Page
"""
@app.route('/search', methods= ['POST', 'GET'] )
def search():
 # query = request.form['q']
  query = request.args.get('q').lower()
  politicians = Politician.all()
  politicians.filter("name =", query)
  politician = None
  for p in politicians:
    politician = p
  return render_template('politician.html', q = query, politician = politician)


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
@app.route('/json/politicians/<politician>')
def json_politician(politician):
  politicians = Politician.all()
  politicians.filter("name =", politician)
  politician = None
  for p in politicians:
    politician = p
  return jsonify(name=politician.name,
    state = politician.state,
    party = politician.party,
    constituency = politician.constituency,
    wiki = politician.wiki_link
    )

"""Creates entry for politicians in the db
    *Note* : Do not run it more than once, will create multiple entries
"""
@app.route('/updatedb/politicians')
def update_all():
  return insert_politicians_in_db()

@app.route('/json/<newspaper>/<query>')
def test(newspaper, query):
	hinduscraper = scrapers[newspaper]
	hinduscraper.getArticleLinks(query)
	hinduscraper.addArticleContent()
	articles = hinduscraper.getArticles()
	return jsonify(articles=articles)

