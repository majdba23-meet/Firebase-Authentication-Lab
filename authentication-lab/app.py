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
  "databaseURL": "https://garden-a152a-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase= pyrebase.initialize_app(irebaseConfig)
auth = firebase.auth()
db = firebase.database()



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
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
	return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		full_name = request.form['text']
		username = request.form['text1']
		bio = request.form['text2']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user= {'full_name' : full_name , "username" : username , "bio" : bio}
			db.child("Users").child(login_session['user']['localId']).set(user)
			return redirect(url_for('add_tweet'))
		except:
		   error = "Authentication failed"
	return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	error = ""
	if request.method == 'POST':
		title = request.form['title']
		text = request.form['text3']
		tweet= {"title" : title , "text3" : text, "uid" : login_session['user']['localId']}
		db.child("tweets").push(tweet)
		return redirect(url_for("tweets"))
	return render_template("add_tweet.html")


@app.route('/all_tweets')
def tweets():
	tweets = db.child("tweets").get().val()
	#db.child("tweets").push(tweets)
	#print(f"\nthese are your tweets, nir is the best TA: {tweets}\n")
	return render_template("tweets.html", tweets= tweets)


if __name__ == '__main__':
	app.run(debug=True)