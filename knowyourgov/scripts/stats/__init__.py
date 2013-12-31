from google.appengine.ext import db
from knowyourgov.models import Politician
from math import ceil
import logging


def get_average(field):
	pols = Politician.all()
	total = 0
	count = 0
	for pol in pols:
		value = getattr(pol, field)
		if value:
			total += getattr(pol, field)
			count += 1
			logging.info(value)
	return total/count

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
		percentile[field] = 100 * float(greater)/float(total)
		percentile[field] = ceil(100 * percentile[field])/100
	return percentile

def get_stats(pol_name):
	query = "SELECT * FROM Politician WHERE name=\'%s\'" %pol_name 
	result = list(db.GqlQuery(query))
	if result:
		pol = result[0]
		fields = ['attendance', 'debates', 'questions', 'bills']
		return get_percentiles(pol, fields)

# def get_stats(pol_name):
# 	query = "SELECT * FROM Politician WHERE name=\'%s\'" % pol_name
# 	result = list(db.GqlQuery(query))
# 	if result:
# 		pol = result[0]
# 	    fields = ['attendance', 'debates', 'questions', 'bills']
# 	    get_percentiles(pol, fields)

