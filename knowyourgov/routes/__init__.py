from flask import Flask, url_for, render_template, request, make_response, jsonify, json, Response

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
  q = Politician.all()
  q.order('-search_count')

  politicians = []

  count = 0
  for politician in q:
    politicians.append(politician)
    count = count + 1
    if count == 8:
      break
  return render_template('home.html', politicians=politicians)

"""User page
"""
@app.route('/user')
def userpage():
  return render_template('user.html')

"""Detects Location
"""
@app.route('/getlocation')
def currentlocation():
  return render_template('getlocation.html')

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

  if politician != None:
    # increment search count by one
    politician.search_count = politician.search_count + 1
    politician.put()
    return render_template('politician.html', q = name, politician = politician)
  else:
    return render_template('politician_notfound.html', q = name)

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

  if politician != None:
    # increment search count by one
    politician.search_count = politician.search_count + 1
    politician.put()
    return render_template('politician.html', q = query, politician = politician)
  else:
    return render_template('politician_notfound.html', q = query)



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
    wiki = politician.wiki_link,
    imageUrl = politician.image_url,
    search_count = politician.search_count
    )

"""Politicians from a particular state
   Format: JSON
"""
@app.route('/json/politicians/state/<state>')
def politicians_by_state(state):
  pols = Politician.all()
  pols.filter("state =", state.lower())
  pols.order('-search_count')

  politicians = []

  for pol in pols:
    politician = {
      'name': pol.name,
      'party': pol.party,
      'state': pol.state,
      'constituency': pol.constituency,
      'wiki': pol.wiki_link,
      'search_count': pol.search_count
    }

    politicians.append(politician)

  return jsonify(politicians = politicians)

"""Array of datums for politicians
   Format: JSON
"""
@app.route('/json/politicians/all')
def all_politicians():
  pols = Politician.all()

  politicians = []

  for pol in pols:
    tokens = pol.name.title().split(' ')
    politician = {
      'value': pol.name.title(),
      'tokens': tokens
    }

    politicians.append(politician)

  # create JSON response
  resp = Response(
    response=json.dumps(politicians),
    status=200,
    mimetype="application/json"
  )

  return resp

"""Creates entry for politicians in the db
    *Note* : Do not run it more than once, will create multiple entries
"""
@app.route('/updatedb/politicians')
def update_all():
  return insert_politicians_in_db()

# @app.route('/updatedb/images')
# def update_images():
#   return fetch_images()

@app.route('/json/<newspaper>/<query>')
def test(newspaper, query):
	hinduscraper = scrapers[newspaper]
	hinduscraper.getArticleLinks(query)
	hinduscraper.addArticleContent()
	articles = hinduscraper.getArticles()
	return jsonify(articles=articles)

