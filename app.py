from flask import Flask, render_template, request, redirect, url_for, session
import urllib.request as urlrequest
import json
import sqlite3, os
from utl.dbfunc import setup, createUser

app = Flask(__name__)

app.secret_key = os.urandom(32)

DB_FILE = "database.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()

setup(c)

@app.route("/")
def root():
    """redirects to home if cookies are already there, otherwise redirects to login"""
    if "userID" in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/login")
def login():
    """return login page"""
    if "userID" in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route("/signup")
def signup():
    """return signup page"""
    if "userID" in session:
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route("/register", methods=["POST"])
def register():
    """registers the user in the database if they don't have cookies. Also makes cookies if they're not already there."""
    error = '';
    if "userID" in session:
        return redirect(url_for('home'))
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    displayname = request.form['displayname']
    email = "{}@stuy.edu".format(request.form['email'])
    c.execute("SELECT username FROM users WHERE username = '%s'" % username);
    a = c.fetchone()
    if a != None:
        error = 'Username Already Taken'
        return render_template('signup.html', error=error);
    if password != password2:
        error = 'Passwords Don\'t Match'
        return render_template('signup.html', error=error);
    createUser(c, username, password, displayname, email)
    db.commit()
    return redirect(url_for('myprofile'))

@app.route("/auth", methods=['POST'])
def auth():
    """Checks cookies for username and password, if it's not there, it checks the entered username and password.
    If they're both correct, it stores them as cookies."""
    if "userID" in session:
        return redirect(url_for('home'))
    username = request.form['username']
    password = request.form['password']
    c.execute("SELECT userID, password FROM users WHERE username = '%s'" % username)
    a = c.fetchone()
    if a == None:
        error = 'Username Not Found'
        return render_template('login.html', error=error)
    if password != a[1]:
        error = 'Password Incorrect'
        return render_template('login.html', error=error)
    session['userID'] = a[0]
    session['username'] = username
    return redirect(url_for('home'))

@app.route("/home")
def home():
    """Returns Home Page"""
    return "Hello World"

@app.route("/myprofile")
def profile():
    """Returns profile page"""
    return "Woah!"

if __name__ == "__main__":
    app.debug = True
    app.run()
