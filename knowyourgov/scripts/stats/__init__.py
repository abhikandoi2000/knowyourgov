from google.appengine.ext import db
from knowyourgov.models import Politician
from math import ceil
import logging


def get_averages(pol, fields):
	pols = Politician.all()
	pols.filter('position =', pol.position)
	total = 0
	count = 0
	averages = {}
	for field in fields:
		for pol in pols:
			value = getattr(pol, field)
			total += getattr(pol, field)
			count += 1
		if not count:
			averages[field] = 0
		else:
			averages[field] = float(total)/count
			averages[field] = ceil(100 * averages[field])/100
	return averages

def get_percentiles(pol, fields):
	pols = Politician.all()
	pols.filter('position =', pol.position)
	percentile = {}
	for field in fields:
		greater = 0.0
		total = 0.0
		pol_value = getattr(pol, field)
		for politician in pols:
			if politician.name != pol.name:
				value = getattr(politician, field)
				total += 1 
				if pol_value > value:
					greater += 1
		if not total:
			percentile[field] = 0
		else:
			percentile[field] = 100 * float(greater)/float(total)
			percentile[field] = ceil(100 * percentile[field])/100
	return percentile

def get_stats(pol_name):
	query = "SELECT * FROM Politician WHERE name=\'%s\'" %pol_name 
	result = list(db.GqlQuery(query))
	stats = {}
	stats['percentiles'] = {}
	if result:
		pol = result[0]
		fields = ['attendance', 'debates', 'questions', 'bills',]
		if pol.position == 'Member of Parliament' and pol.startofterm == '18-May-09' and pol.endofterm == 'In office':
			stats['percentiles'] = get_percentiles(pol, fields)
			stats['averages'] = get_averages(pol, fields)
			for field in fields:
				stats[field] = getattr(pol, field)
			return stats
		else:
			return ''


# def get_stats(pol_name):
# 	query = "SELECT * FROM Politician WHERE name=\'%s\'" % pol_name
# 	result = list(db.GqlQuery(query))
# 	if result:
# 		pol = result[0]
# 	    fields = ['attendance', 'debates', 'questions', 'bills']
# 	    get_percentiles(pol, fields)