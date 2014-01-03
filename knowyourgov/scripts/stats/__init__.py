from google.appengine.ext import db
from knowyourgov.models import Politician
from math import ceil
import logging
  
fields = ['attendance', 'debates', 'questions', 'bills']
wealth_fields = ['net_worth', 'cash', 'property', 'other']
# def get_averages(pol, fields, filters):
# 	pols = Politician.all()
# 	pols.filter('position =', pol.position)
# 	for filter_ in filters:
# 		pols.filter(filter_['property'], filter_['value'])
# 	averages = {}
# 	for field in fields:
# 		total = 0
# 		count = 0
# 		for pol in pols:
# 			total += getattr(pol, field)
# 			count += 1
# 		if not count:
# 			averages[field] = 0
# 		else:
# 			averages[field] = float(total)/count
# 			averages[field] = ceil(100 * averages[field])/100
# 		logging.info(averages)
# 	return averages

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
		logging.info(averages)
	return averages

def get_percentiles(pol, fields, filters):
	pols = Politician.all()
	pols.filter('position =', pol.position)
	for filter_ in filters:
		pols.filter(filter_['property'], filter_['value'])
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
