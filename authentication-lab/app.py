from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyD4Zc1bLQ_v3gx81g3Brp7NLngi2C8ZeGs",
  "authDomain": "cs-week-2-day-1.firebaseapp.com",
  "databaseURL": "https://cs-week-2-day-1-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "cs-week-2-day-1",
  "storageBucket": "cs-week-2-day-1.appspot.com",
  "messagingSenderId": "386419703402",
  "appId": "1:386419703402:web:f7e360594c2e9cb4fe9413",
  "measurementId": "G-0LPHE23XL3"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
        except:
           error = "Authentication failed"
        return redirect(url_for('add_tweet'))
    else:
        return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
        password = request.form['password']
        user = {"email" : email, "name": full_name, "username" : username, "bio" : bio, "password" : password}
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            db.child('Users').child(login_session['user']['localId']).set(user)
        except:
           error = "operation failed"
        return redirect(url_for('add_tweet'))
    else:
        return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        uid= db.child('Users').child(login_session['user']['localId']).get().val()
        tweet = {"title" : title, "text" : text, "uid" : uid}
        try:
            db.child('Tweets').push(tweet)
        except:
            error = "operation failed"
    return render_template("add_tweet.html")

@app.route('/tweets', methods=['GET', 'POST'])
def tweets():

    return render_template("tweets.html", tweets = db.child('Tweets').get().val())



if __name__ == '__main__':
    app.run(debug=True)