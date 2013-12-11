from google.appengine.ext import db
from knowyourgov.models import Politician
import csv
import json

def update_data_from_csv():
  q = db.Query(Politician)
  with open('datasets/members.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    x=[]
    for row in reader:
      #'''Lok Sabha,Member Name,Gender,Constituency Name,Party Name,State Name,Date of Birth,Marital Status,Freedom Fighter,Permanent Address,Permanent Phone,Delhi Address,Delhi Phone,Profession,Father Name,Mother Name,Spouse Name,Place of Birth,Date of Marriage,No. of Sons,No. of Daughters,Education & Institution,Books Published,Literary Interest,Social And Cultural Activities,Special Interests,Hobbies,Sports,Countries Visited,Other Information'''
      pols = Politician.all()
      pols.filter("constituency =", row[3].strip().lower())
      if pols:
        try:
          pol = list(pols)[0]
          x.append({
            'name': pol.name,
            'dob' : row[6],
            'gender': row[2]
            })
          pol.gender = 2 if row[2] == 'Female' else 1
          if not row[6] == 'NA':
            pol.dob = row[6]
          pol.put()
        except Exception, e:
          pass
  # return json.dumps(x)
  return "Gender and DOB updated for %d entries." % (len(x))