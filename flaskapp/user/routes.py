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

  

# @app.route('/user/login', methods=['POST','GET'])
# def scrape():
#   return scrapped_page()
# @app.route('/dashboard/scrapped', methods=['POST','GET'])
# def scrapped():
#   num =20
#   hashtag = request.form.get('hashtag')
#   date=""
#   return scrape(hashtag,date,num)