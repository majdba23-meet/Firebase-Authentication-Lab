from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


irebaseConfig = {
  "apiKey": "AIzaSyC7be0MkeMQRPZLbc8xcrzVygtcoAeQvcM",
  "authDomain": "garden-a152a.firebaseapp.com",
  "projectId": "garden-a152a",
  "storageBucket": "garden-a152a.appspot.com",
  "messagingSenderId": "232233415044",
  "appId": "1:232233415044:web:7bbc44aad6092724032dd1",
  "measurementId": "G-5ZY1B9BZB5",
  "databaseURL": ""
}

firebase= pyrebase.initialize_app(irebaseConfig)
auth = firebase.auth()

app = Flask(__name__)



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
       except:
           error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('home'))
       except:
           error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)