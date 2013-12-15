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
          if not row[11] == 'N/A':
            pol.debates = int(row[11])
          if not row[12] == 'N/A':
            pol.bills = int(row[12])
          if not row[13] == 'N/A':
            pol.questions = int(row[13])
          if not row[14] == 'N/A':
            pol.attendance = row[14]
          pol.put()
          # break
        except Exception, e:
          pass
  # return json.dumps(x)
  return "Gender and DOB updated for %d entries." % (len(x))