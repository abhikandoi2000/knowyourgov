from flask import Flask, url_for, render_template, request, make_response, jsonify, json, Response, redirect
import requests
from requests_oauthlib import OAuth1
from google.appengine.api import taskqueue

from knowyourgov import app
from knowyourgov.models import Politician, Party
from knowyourgov.scripts import insert_politicians_in_db
from knowyourgov.scripts import stats
from knowyourgov.scripts.data import update_csvdata_in_db, update_scrapeddata_in_db, add_party_details_db
from knowyourgov.scripts.scraping import scrapers
# import errors

"""Home page
"""
@app.route('/')
def homepage():
  q = Politician.all()
  q.order('-search_count')
  politicians = list(q[:8]) or []
  return render_template('home.html', politicians=politicians)

"""About Page + Feedback
"""
@app.route('/about')
def aboutpage():
  return render_template('about.html')

"""Detects Location
"""
@app.route('/getlocation')
def currentlocation():
  return render_template('getlocation.html')

"""Politician Page
"""
@app.route('/politicians/id/<name>')
def politician_page(name):
  #Checks for blank between in politician page and redirects, so as to have a unique page for every politician
  if ' ' in name:  
    name = name.replace(' ', '-')
    return redirect('/politicians/id/'+ name)
  
  name = name.lower().replace('-',' ')
  politicians = Politician.all()
  politicians.filter("name =", name)
  politician = list(politicians[:1])
  if politician:
    politician = politicians[0]
    # increment search count by one
    politician.search_count = politician.search_count + 1
    politician.put()
    # Format Wealth 
   
    net_worth = '{:20,.0f}'.format(politician.net_worth)

    try:
      politician.first_name, politician.last_name = politician.name.split(' ')[0:2]
    except:
      politician.first_name = politician.name
      politician.last_name = ''
    return render_template('politician.html', q = name, politician = politician, title = name, net_worth= net_worth)
  else:
    return render_template('politician_notfound.html', q = name)

"""Search -> Politician Page
"""
@app.route('/search', methods= ['POST', 'GET'] )
def search():
 # query = request.form['q']
  query = request.args.get('q').lower().replace('-',' ')
  politicians = Politician.all()
  politicians.filter("name =", query)
  politician = list(politicians[:1])
  if politician:
    politician = politicians[0]
    name = query.replace(' ','-')
    return redirect('/politicians/id/'+name)
  else:
    return render_template('politician_notfound.html', q = query)


@app.route('/state/<state>')
def state(state):
  state = state.lower().replace('-',' ')
  pols = Politician.all()
  pols.filter("state =", state)
  pols.order('-search_count')
  return render_template('politician_list.html', politicians = pols, title="List of politicians in "+state)

@app.route('/parties')
def party_landing():
  parties = Party.all()
  return render_template('party_landing.html', parties = parties)

@app.route('/party/<party>')
def party(party):
  if ' ' in party:  
    party = party.replace(' ', '-')
    return redirect('/party/'+ party)


  if len(party) < 2:
    return redirect('/parties')
      
  party = party.lower().replace('-',' ')
  pols = Politician.all()
  pols.filter("party =", party)
  pols.order('-search_count')
  parties = Party.all()
  parties.filter("name =", party)
  
  """
  channel = parties[0].youtube[24:]
  app.logger.debug(channel)
  #Configuring to fetch requests

  payload = { 'alt' : 'jsonc' , 'max-results' : '3' , 'v' : '2' }
  r  = requests.get('https://gdata.youtube.com/feeds/api/users/' + str(channel) + '/uploads')

  vid = []

  if r.status_code == 200 :
    app.logger.debug(r.content())
  
    c = r.content()

    for i in c.data.items : 
      obj = { 'id' : c.data.items[i].id , 'title' : c.data.items[i].title }
      vid.append(obj)
  """

  return render_template('party.html', politicians = pols, title=party, parties=parties)

"""Initial page for stats for politicians
"""
@app.route('/stats/politician/<name>', methods=['GET'])
def pol_stats(name):
  if ' ' in name:  
    name = name.replace(' ', '-')
    return redirect('/stats/politician/'+ name)

  name = name.lower().replace('-',' ')
  pol_stats = stats.get_stats(name, stats.pol_fields)
  wealth_stats = stats.get_stats(name, stats.wealth_fields)
  return render_template('stats.html', pol_stats = pol_stats, wealth_stats = wealth_stats, fields = stats.pol_fields, wealth_fields = stats.wealth_fields, name = name)

@app.route('/stats/state/<state>', methods=['GET'])
def state_stats(state):
  state = state.lower().replace('-',' ')
  state_stats = stats.get_state_stats(state)
  return jsonify(state_stats)
  
"""
   ** Error Handlers **
   404, 500 and other errors
"""

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


"""
   ** JSON response routes **
"""

"""JSON response containing information for a particular politician
"""
@app.route('/json/politicians/<name>', methods=['GET'])
def json_politician(name):
  name = name.replace('-', ' ').lower()
  politicians = Politician.all()
  politicians.filter("name =", name)
  politician = list(politicians)

  if politician:
    politician = politician[0]
    return jsonify(name=politician.name,
      state = politician.state,
      party = politician.party,
      constituency = politician.constituency,
      wiki = politician.wiki_link,
      imageUrl = politician.image_url,
      search_count = politician.search_count
      )
  else:
    return jsonify(message="error",
      reason="politician_not_found"
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
      'tokens': tokens,
      'search_count': pol.search_count
    }

    politicians.append(politician)

  # create JSON response
  resp = Response(
    response=json.dumps(politicians),
    status=200,
    mimetype="application/json"
  )

  return resp

"""News articles from various news sources
   Format: JSON
"""
@app.route('/json/<newspaper>/<query>')
def test(newspaper, query):
	hinduscraper = scrapers[newspaper]
	hinduscraper.getArticleLinks(query)
	hinduscraper.addArticleContent()
	articles = hinduscraper.getArticles()
	return jsonify(articles=articles)

"""Tweets for a search query
   Format: JSON
"""
@app.route('/json/tweets/search/<query>', methods=['GET'])
def tweets_search(query):
  # oauth tokens for Twitter APP
  access_token = '487593326-yu9WIClcUgs9vBWJGGgW4QC9pKedHMdm3NhhNoxe'
  access_token_secret = 'fMcsDcqTtbeM73qB7Cxo7dGKhZT9byGh7i5lKjOVscQzP'
  consumer_key = 'yd6lDwm3Ra9j7djyXHmrg'
  consumer_secret = 'BlBMf6kP98LwWepOVSypVwDi2x2782P2KQnJQomY'

  oauth = OAuth1(consumer_key,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
    client_secret=consumer_secret
    )

  base_url = 'https://api.twitter.com/1.1/'
  search_url = 'search/tweets.json'
  verify_url = 'account/verify_credentials.json'
  payload = {'q': query, 'count': '5', 'lang': 'en', 'result_type': 'mixed', '+exclude': 'retweets'}

  # verify account credentials
  response = requests.get(base_url + verify_url, auth=oauth)
  if response.status_code == 200:
    response = requests.get(base_url + search_url, params=payload, auth=oauth)

    # create JSON response
    resp = Response(
      response=response.content,
      status=200,
      mimetype="application/json"
    )
    
    return resp
  else:
    return jsonify(error=str(response.content))

"""Stats for politicians
   Format: JSON
"""
@app.route('/json/stats/politician/<name>', methods=['GET'])
def pol_statsjson(name):
  name = name.lower().replace('-',' ')
  return jsonify(stats.get_stats(name, stats.pol_fields))

"""
   **Database errands**

"""

"""Creates entry for politicians in the db
    *Note* : Do not run it more than once, will create multiple entries
"""
@app.route('/updatedb/politicians')
def update_all():
  """
  Method @insert_politicians_in_db
  scripts/ __init__.py
  Fields Updated
  -name
  -party
  -state
  -constituency
  -position
  -wiki_link
  -image_url
  -search_count (Default is 0 for everyone)
  """
  return insert_politicians_in_db()

@app.route('/updatedb/csvdata')
def update_csvdata():
  """
  Method @update_csvdata_in_db
  scripts/data/__init__.py
  Fields Updated
  -Gender
  -Age
  -Term details
  -Education
  -Debates
  -Bills
  -Questions
  -Attendance
  """
  return update_csvdata_in_db()

@app.route('/updatedb/scrapeddata', methods=['POST'])
def update_scrapeddata():
  return update_scrapeddata_in_db()

@app.route('/updatedb/partyinfo')
def add_party_data():
  return add_party_details_db()

@app.route('/enqueue/updatedb/scrapeddata')
def enqueue_update_scrapeddata():
  taskqueue.add(url='/updatedb/scrapeddata')
  self.redirect('/')

