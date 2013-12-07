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
      q = Politician.all()
      #x.append(row[3].lower())
      q.filter("constituency=",row[3].lower())
      result = q.get()
      x.append(result)
      #'''Lok Sabha,Member Name,Gender,Constituency Name,Party Name,State Name,Date of Birth,Marital Status,Freedom Fighter,Permanent Address,Permanent Phone,Delhi Address,Delhi Phone,Profession,Father Name,Mother Name,Spouse Name,Place of Birth,Date of Marriage,No. of Sons,No. of Daughters,Education & Institution,Books Published,Literary Interest,Social And Cultural Activities,Special Interests,Hobbies,Sports,Countries Visited,Other Information'''
      #constituency = row[3]
      #p=pols.filter('constituency=',row[3].lower())
      #p = list(pols[:1])
      #if(p):
      #  result=p[0] #Get first result
      #  #print p[0].name+"\n"
      #  result.gender = int(row[2]=='Male') #0=Female, 1 =Male (True default)
      #  result.dob = row[6]
      #  result.put()
      #else:
        #print "Not Found\n"
  return json.dumps(x)