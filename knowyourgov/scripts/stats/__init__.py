from google.appengine.ext import db
from knowyourgov.models import Politician
from math import ceil
import logging
  
pol_fields = ['attendance', 'debates', 'questions']
wealth_fields = ['net_worth', 'cash', 'property', 'other']
state_fields = ['gender', 'age', 'party']
party_fields = ['gender', 'age']

def get_averages(pols, fields):
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

def get_percentiles(pol, pols, fields):
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

def get_stats(pol_name, fields, filters = []):
	pols = Politician.all()
	for filter_ in filters:
		pols.filter(filter_['property'], filter_['value'])

	stats = {}
	pol = Politician.all().filter('name =', pol_name)[0]
	pols.filter('position =', pol.position)

	if pol.position == 'Member of Parliament' and pol.startofterm == '18-May-09' and pol.endofterm == 'In office':
		stats['percentiles'] = get_percentiles(pol, pols, fields)
		stats['averages'] = get_averages(pols, fields)
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
	return distribution

def get_party_stats(party_name, filters = []):
	pols = Politician.all()
	pols.filter('party =', party_name)
	for filter_ in filters:
		pols.filter(filter_['property'], filter_['value'])
	distribution = {}
	for field in party_fields:
		distribution[field] = get_distribution(pols, field)
	return distribution		

def get_distribution(pols, field):
	distribution = {}
	for pol in pols:
		key = getattr(pol, field)
		if not key:
			continue
		if field == 'gender':
			key = pol.gender_str()
		if field == 'age':
			key = str(key/10 *10)+'-'+str((key/10 + 1)*10 - 1)
		if not(key in distribution.keys()):
			distribution[key] = 0
		distribution[key] +=1
	return distribution