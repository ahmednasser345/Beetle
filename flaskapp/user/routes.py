from flaskapp import app 
from flask import jsonify , request , session
from flaskapp.user.models import User,ScrapeTwitter,ScrapeInstagram
import requests
import pandas as pd
import csv
@app.route('/user/signup', methods=['POST','GET'])
def signup():
  return User().signup()

@app.route('/user/signout', methods=['POST','GET'] )
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST','GET'])
def login():
  return User().login()
@app.route('/dashboard/twitter', methods=['GET'])
def scrape():
  return ScrapeTwitter().scrape()


@app.route('/dashboard/instagram', methods=['GET'])
def scrape_instagram():
  return ScrapeInstagram().getPosts()

@app.route('/annotate/saveAnnotation', methods=['POST'])
def saveAnnotation():
  global annotation1
   
   
  print(request.json['annotationss'])
  annotation1 = request.json['annotationss']
  df=pd.DataFrame(annotation1)   
  #annotation1.append(request.json['annotationss'])
  
  currentUser=session['user']['email']
  filename=currentUser+'-annotations.csv'
  csv_file = filename

  df.to_csv(filename)
  




  currentUserScraped=session['user']['email']+'.csv'
  currentUserannotations=session['user']['email']+'-annotations.csv'
  
  file1 = open(currentUserScraped)
  file2 = open(currentUserannotations)

  #create a csv reader for each file

  csv1 = csv.reader(file1)
  csv2 = csv.reader(file2)


  #create an empty list to store the data

  combined_file = []

  #add the contents of both csv files to the combined_file list

  for row in csv1:
      combined_file.append(row)
      
  for row in csv2:
      combined_file.append(row)

  #open a new file to store the combined data
  combinedfile = session['user']['email']+'allData.csv'
  file3 = open(combinedfile, "w")

  #create a csv writer

  csv3 = csv.writer(file3)

  #write the contents of the combined_file list to the new file

  for row in combined_file:
      csv3.writerow(row)

  #close all files
    
  return jsonify({'error': 'Annotation error!'}), 200

  

