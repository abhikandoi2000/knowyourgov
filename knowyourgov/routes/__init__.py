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

STATES = ['Haryana', 'Punjab', 'Goa', 'Chhattisgarh', 'Kerala', 'Daman and Diu', 'Bihar', 'Tamil Nadu', 'Chandigarh', 'Jammu and Kashmir', 'Dadra and Nagar Haveli', 'Jharkhand', 'Meghalaya', 'Delhi', 'Assam', 'Madhya Pradesh', 'Lakshadweep', 'Manipur', 'Rajasthan', 'Sikkim', 'West Bengal', 'Andhra Pradesh', 'Himachal Pradesh', 'Nagaland', 'Gujarat', 'Arunachal Pradesh', 'Maharashtra', 'Tripura', 'Uttarakhand', 'Puducherry', 'Karnataka', 'Jammu & Kashmir', 'Mizoram', 'Odisha', 'Uttar Pradesh', 'Andaman and Nicobar Islands']

"""Home page
"""
@app.route('/')
def homepage():
  q = Politician.all()
  q.order('-search_count')
  politicians = list(q[:4]) or []
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
  query = request.args.get('q')
  if query.title() in STATES:
    state = query.lower().replace(' ', '-')
    return redirect('/state/' + state)
  query = query.lower().replace('-', ' ')
  politicians = Politician.all()
  politicians.filter("name =", query)
  politician = list(politicians[:1])
  if politician:
    politician = politicians[0]
    name = query.replace(' ', '-')
    return redirect('/politicians/id/' + name)
  else:
    parties = Party.all()
    parties.filter("name =", query)
    party = list(parties[:1])
    if party:
      party = party[0]
      name = query.lower().replace(' ', '-')
      return redirect('/party/' + name)
    else:
      return render_template('politician_notfound.html', q = query)


@app.route('/state/<state>')
def state(state):
  state = state.lower().replace('-',' ')
  state_stats = stats.get_state_stats(state)
  pols = Politician.all()
  pols.filter("state =", state)
  pols.order('-search_count')
  return render_template('politician_list.html', politicians = pols, stats = state_stats, title="List of politicians in " + state)

@app.route('/states')
def state_landing():
  states = []
  for s in STATES:
    politicians = Politician.all()
    politicians.filter("state = ", s.lower())
    politicians = list(politicians)
    male_pols = [politician for politician in politicians if politician.gender == 1]
    female_pols = [politician for politician in politicians if politician.gender == 2]
    state = {
      'name': s,
      'pol_count': len(politicians),
      'male_pol_count': len(male_pols),
      'female_pol_count': len(female_pols) 
    }
    states.append(state)
  return render_template('state_landing.html', states = states)

@app.route('/parties')
def party_landing():
  parties = Party.all()
  return render_template('party_landing.html', parties = parties)

@app.route('/party/<party>')
def party(party):
  if ' ' in party:  
    party = party.replace(' ', '-')
    return redirect('/party/'+ party)

  party = party.lower().replace('-',' ')
  party_stats = stats.get_party_stats(party)
  pols = Politician.all()
  pols.filter("party =", party)
  pols.order('-search_count')

  parties = Party.all()
  parties.filter("name =", party)

  app.logger.debug(parties.count())

  if parties.count() == 0:
    return render_template('party.html', politicians = pols, title=party)

  app.logger.debug('2')
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

  return render_template('party.html', politicians = pols, stats=party_stats, title=party, parties=parties)

"""Initial page for stats for politicians
"""
@app.route('/stats/politician/<name>', methods=['GET'])
def pol_stats(name):
  if ' ' in name:  
    name = name.replace(' ', '-')
    return redirect('/stats/politician/'+ name)
    
  name = name.lower().replace('-',' ')
  politicians = Politician.all()
  politicians.filter("name =", name)
  politician = list(politicians[:1])
  if politician:
    politician = politicians[0]
  pol_stats = stats.get_stats(name, stats.pol_fields)
  wealth_stats = stats.get_stats(name, stats.wealth_fields)
  return render_template('stats.html', politician = politician, pol_stats = pol_stats, wealth_stats = wealth_stats, fields = stats.pol_fields, wealth_fields = stats.wealth_fields, name = name)

@app.route('/stats/state/<state>', methods=['GET'])
def state_stats(state):
  state = state.lower().replace('-',' ')
  state_stats = stats.get_state_stats(state)
  return jsonify(state_stats)
  
@app.route('/stats/party/<party>', methods=['GET'])
def party_stats(party):
  party = party.lower().replace('-',' ')
  state_stats = stats.get_party_stats(party)
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

"""Array of datums for parties
   Format: JSON
"""
@app.route('/json/parties/all', methods=['GET'])
def all_parties():
  result = Party.all()

  parties = []

  for party in result:
    tokens = party.name.title().split(' ')
    parti = {
      'value': party.name.title(),
      'tokens': tokens,
    }

    parties.append(parti)

  # create JSON response
  resp = Response(
    response=json.dumps(parties),
    status=200,
    mimetype="application/json"
  )

  return resp

"""Array of datums for states
   Format: JSON
"""
@app.route('/json/states/all')
def all_states():
  datums = []

  for state in STATES:
    tokens = state.title().split(' ')
    stat = {
      'value': state.title(),
      'tokens': tokens,
    }

    datums.append(stat)

  # create JSON response
  resp = Response(
    response=json.dumps(datums),
    status=200,
    mimetype="application/json"
  )

  return resp

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

