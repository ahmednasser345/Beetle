from flaskapp import app
from flaskapp.user.models import User,ScrapeTwitter

@app.route('/user/signup', methods=['POST','GET'])
def signup():
  return User().signup()

@app.route('/user/signout', methods=['POST','GET'] )
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST','GET'])
def login():
  return User().login()
@app.route('/dashboard/scrapped', methods=['GET'])
def scrape():
  return ScrapeTwitter().scrape()

  

