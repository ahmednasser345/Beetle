from flask import render_template, redirect, url_for, request, jsonify ,send_file , session
from flaskapp import app, login_required, db
from flaskapp.user.routes import *
from werkzeug.utils import secure_filename
import pandas as pd
import json
import uuid
import csv


@app.route('/')
def home():
  return render_template('home.html')

@app.route('/login')
def login_page():
  return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
  labels = []
  print(session['user'])
  try:
    currentUser= db.users.find_one({'_id': session["user"]["_id"]})
    print(currentUser)
    print("CURRENT",currentUser['labels'])
    labels=currentUser['labels']
  except:
    return jsonify({'error': 'DB error!'}), 400

  return render_template('profile.html', labels=labels)

@app.route('/profile/addLabel')
@login_required
def add_label():
  return render_template('add-label.html')

@app.route('/dashboard')
@login_required
def dashboard():
  return render_template('dashboard.html')



@app.route('/collect')
@login_required
def collect_page():
  return render_template('collect.html')


@app.route('/choose')
@login_required
def choose_page():
  return render_template('choose.html')




@app.route('/annotate')
@login_required
def annotate_page():
  labels = []
  try:
    currentUser= db.users.find_one({'_id': session["user"]["_id"]})
    labels=currentUser['labels']
  except:
    return jsonify({'error': 'DB error!'}), 400

  try:
    filename=session['user']['email']+'.csv'
    data = pd.read_csv(filename)
    data.rename( columns={'Unnamed: 0':'ID'}, inplace=True ) 
  except:
    return redirect(url_for('dashboard'))

  tweets:list = data.to_dict('list')
  return render_template('annotate.html', tweets=tweets, labels = labels)


@app.route('/annotate/upload', methods = ['POST','GET'])
@login_required
def annotate_upload():
  labels = []
  try:
    currentUser= db.users.find_one({'_id': session["user"]["_id"]})
  
    labels=currentUser['labels']
  except:
    return jsonify({'error': 'DB error!'}), 400
  
  if request.method == 'POST':
    tweets: list = []
    upload_file = request.files['upload_file']

    if upload_file.filename != '':
      upload_file.save(secure_filename('uploaded_tweets.csv'))
      
      try:
        data = pd.read_csv('uploaded_tweets.csv')
        data.rename( columns={'Unnamed: 0':'ID'}, inplace=True )     
        tweets = data.to_dict('list')
      except:
        return render_template('annotate.html', error='Unsupported file format! Try again.')

    return render_template('annotate.html', tweets=tweets,labels = labels)

  
@app.route('/download')
@login_required
def download_file():
	currentUser=session['user']['email']
  
	path = "../"+currentUser+'.csv'

	return send_file(path, as_attachment=True)


@app.route('/profile/saveNewLabel')
@login_required
def save_new_label():
  label = request.args.get('label')


  
  if  db.users.update_one({ "_id": session['user']['_id'] },{ "$push": { "labels": label }}):
    return jsonify({'success': 'A label is saved successfully!'}), 200 

  return jsonify({ "error": "Adding a new label is failed" }), 400


@app.route('/instagram')
def instagram_page():
  return render_template('instagram.html')


if __name__ == '__main__':
  app.run(host = "0.0.0.0",port = 3000, debug=True)
