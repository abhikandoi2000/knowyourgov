from google.appengine.ext import db
from knowyourgov.models import Politician
from knowyourgov.scripts.scraping import scrapers
import csv
import json
import logging


def update_csvdata_in_db():
  st = ""
  st += update_data_from_csv()
  st += update_data_from_csv2()
  return st

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
            'gender': row[2]
            })
          pol.gender = 2 if row[2] == 'Female' else 1
          pol.put()
        except Exception, e:
          pass
  # return json.dumps(x)
  return "Gender updated for %d entries." % (len(x))

def update_data_from_csv2():
  q = db.Query(Politician)
  with open('datasets/MPTrack-15.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    x=[]
    for row in reader:
      #MP name,Nature of membership,Start of term,End of term,State,Constituency,Political party,Gender,Educational qualifications,
      #Educational qualifications - details,Age,Debates,Private Member Bills,Questions,Attendance,Notes,National Debates average,
      #National Private Member Bills average,National Questions average,National Attendance average,State's Debates average,
      #State's Private Member Bills  average,State's Questions average,State's Attendance average

      pols = Politician.all()
      pols.filter("constituency =", row[5].strip().lower())
      if pols:
        try:
          pol = list(pols)[0]
          x.append({
            'name': pol.name,
            'membership' : row[1],
            'startofterm' : row[2],
            'endofterm' : row[3],
            'education' : row[9],
            'age' : row[10],
            'debates' : row[11],
            'bills' : row[12],
            'questions' : row[13],
            'attendance' : row[14]
            })

          pol.membership = row[1]
          if not row[2] == 'N/A':
            pol.startofterm = row[2]
          if not row[3] == 'N/A':
            pol.endofterm = row[3]
          if not row[9] == 'N/A':
            pol.education = row[9]
          if not row[10] == 'N/A':
            pol.age = int(row[10])
          if not row[11] == 'N/A':
            pol.debates = int(row[11])
          if not row[12] == 'N/A':
            pol.bills = int(row[12])
          if not row[13] == 'N/A':
            pol.questions = int(row[13])
          if not row[14] == 'N/A':
            pol.attendance = int(row[14][:-1])
          pol.put()
          # break
        except Exception, e:
          pass
  # return json.dumps(x)
  return "Age, term details, education, debates, bills, questions and attendance updated for %d entries." % (len(x))

def update_scrapeddata_in_db():
  x = []
  with open('datasets/india60links.txt') as f:
    links = f.readlines()

  for link in links:    
    logging.info("Fetching data from "+link)
    try:
      polData = scrapers['india60'].getPoliticianData(link)
    except Exception, e:
      return str(e)
    query = db.GqlQuery("SELECT * FROM Politician WHERE constituency=\'"+polData['constituency'].lower()+"\'")
    pol = query[0]
    for key, value in polData['wealth'].iteritems():
      setattr(pol, key, value)
    pol.official_link = polData['official_link']
    pol.put()
    x.append(polData)
    break

  return json.dumps(x)