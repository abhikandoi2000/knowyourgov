from google.appengine.ext import db
from knowyourgov.models import Politician
from math import ceil
import logging
  
fields = ['attendance', 'debates', 'questions', 'bills']
wealth_fields = ['net_worth', 'cash', 'property', 'other']
state_fields = ['gender', 'age', 'party']

def get_averages(pol, fields, filters):
	pols = Politician.all()
	pols.filter('position =', pol.position)
	for filter_ in filters:
		pols.filter(filter_['property'], filter_['value'])
	averages = {}
	total = {}
	count = 0
	for pol in pols:
		for field in fields:
			if not (field in total.keys()):
				total[field] = 0
			total[field] += getattr(pol, field)
		count += 1
	for field in fields:	
		if not count:
			averages[field] = 0
		else:
			averages[field] = float(total[field])/count
			averages[field] = ceil(100 * averages[field])/100
	return averages

def get_percentiles(pol, fields, filters):
	pols = Politician.all()
	pols.filter('position =', pol.position)
	for filter_ in filters:
		pols.filter(filter_['property'], filter_['value'])
	percentile = {}
	greater = {}
	total = 0
	for politician in pols:
		total += 1 
		for field in fields:
			if not(field in greater.keys()):
				greater[field] = 0
			pol_value = getattr(pol, field)
			if politician.name != pol.name:
				value = getattr(politician, field)
				if pol_value > value:
					greater[field] += 1
	for field in fields:
		if not total:
			percentile[field] = 0
		else:
			percentile[field] = 100 * float(greater[field])/float(total)
			percentile[field] = ceil(100 * percentile[field])/100
	return percentile

def get_stats(pol_name, filters, fields):
	query = "SELECT * FROM Politician WHERE name=\'%s\'" %pol_name 
	result = list(db.GqlQuery(query))
	stats = {}
	stats['percentiles'] = {}
	if result:
		pol = result[0]
		if pol.position == 'Member of Parliament' and pol.startofterm == '18-May-09' and pol.endofterm == 'In office':
			stats['percentiles'] = get_percentiles(pol, fields, filters)
			stats['averages'] = get_averages(pol, fields, filters)
			for field in fields:
				stats[field] = getattr(pol, field)
			return stats
		else:
			return ''

def get_state_stats(state, filters = []):
	pols = Politician.all()
	pols.filter('state =', state)
	for filter_ in filters:
		pols.filter(filter_['property'], filter_['value'])
	distribution = {}
	for field in state_fields:
		distribution[field] = get_distribution(pols, field)
	logging.info(distribution)
	return distribution

def get_distribution(pols, field):
	distribution = {}
	for pol in pols:
		value = getattr(pol, field)
		if not value:
			continue
		if not(value in distribution.keys()):
			distribution[value] = 0
		distribution[value] +=1
	return distribution
