from flask import Flask, render_template, request, redirect, url_for, session
import urllib.request as urlrequest
import json
import sqlite3, os
import random
from utl.dbfunc import setup, createUser, getSchedule, update_user
import utl.dbfunc as dbfunc


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
        return render_template('signup.html', error=error, message='Please choose a different name.');
    if password != password2:
        error = 'Passwords Don\'t Match'
        return render_template('signup.html', error=error, message='Make sure to confirm your password correctly!');
    createUser(c, username, password, displayname, email, "/static/MykPic.jpg")
    db.commit()
    c.execute("SELECT userID, username FROM users WHERE username = '%s'" % username)
    a = c.fetchone()
    session['userID'] = a[0]
    session['username'] = a[1]
    session['registered'] = True
    return redirect(url_for('profile'))

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
        return render_template('login.html', error=error, message="Did you enter the right username?")
    if password != a[1]:
        error = 'Password Incorrect'
        return render_template('login.html', error=error, message="Wrong password... it happens to the best of us.")
    session['userID'] = a[0]
    session['username'] = username
    return redirect(url_for('home'))

@app.route("/home")
def home():
    """Returns Home Page"""
    if "userID" not in session:
        return redirect(url_for('login'))
    return render_template('home.html', user=session["username"])

@app.route("/myprofile")
def profile():
    """Returns profile page"""
    if "userID" not in session:
        return redirect(url_for('login'))
    if "registered" in session:
        message = True
        session.pop("registered")
    else:
        message = False
    c.execute("SELECT username, displayName, image, email FROM users WHERE userID = '{}'".format(session['userID']))
    bruh = c.fetchone()
    schedule = getSchedule(c, session["userID"])
    print(schedule)
    print(bruh)
    return render_template('profile.html', username = bruh[0],
                                           displayName = bruh[1],
                                           schedule = schedule,
                                           image = bruh[2],
                                           email = bruh[3], message=message)

@app.route("/mygroups")
def mygroups():
    """Returns Home Page"""
    if "userID" not in session:
        return redirect(url_for('login'))
    return render_template('mygroups.html', user=session["username"])

@app.route("/settings")
def settings():
    if "userID" not in session:
        return redirect(url_for('login'))
    if "e1" not in session:
        session["e1"] = False
    if "e2" not in session:
        session["e2"] = False
    if "message" not in session:
        session["message"] = ""
    return render_template('settings.html', e1 = session["e1"], e2 = session["e2"], message=session["message"]);

@app.route("/change_settings", methods=["POST"])
def changing():
    session["e1"] = False
    session["e2"] = False
    if "userID" not in session:
        return redirect(url_for('login'))
    if (request.form['check_password'] == ''):
        if (request.form['new_password'] != '' or request.form['confirm_password'] != ''): #if other password fields filled out, something's wrong
            session["e2"] = True
            session["message"]="Necessary Fields Not Filled Out"
            return redirect(url_for('settings'))
        # change Username
        if (request.form['newusername'] == ''): #if username fields not filled out, something's wrong
            session["e1"] = True
            session["message"]="Necessary Fields Not Filled Out"
            return redirect(url_for('settings'))
        c.execute("SELECT username FROM users WHERE username = '%s'" % request.form['newusername'])
        a = c.fetchone()
        if (a != None): #username is in database already
            session["e1"] = True
            session["message"]="Username Already Taken"
            return redirect(url_for('settings'))
        update_user(session['username'], "username", request.form['newusername']) #updating the database imported
        session['username'] = request.form['newusername']
        return render_template('settings.html', changed1=True)
    else: # password being changed
        if (request.form['new_password'] == '' or request.form['confirm_password'] == ''): #if password fields not filled out, something's wrong
            session["e2"] = True
            session["message"]="Necessary Fields Not Filled Out"
            return redirect(url_for('settings'))
        c.execute("SELECT password FROM users WHERE username = '%s'" % session['username'])
        a = c.fetchone()
        if (request.form['check_password'] != a[0]): #old password not correct
            session["e2"] = True
            session["message"]="Incorrect Password"
            return redirect(url_for('settings'))
        if (request.form['new_password'] != request.form['confirm_password']): #passwords don't match
            session["e2"] = True
            session["message"]="Passwords Don't Match"
            return redirect(url_for('settings'))
        update_user(session['username'], "password", request.form['new_password']) #updating the database
        return render_template('settings.html', changed2=True)

@app.route("/logout")
def logout():
    """Removes user session, redirects to login page"""
    if 'userID' in session:
        session.clear()
        return redirect(url_for("login"))
    return redirect(url_for("root"))

@app.route("/games")
def games():
    """Returns Games Page"""
    if "userID" not in session:
        return redirect(url_for('login'))
    return render_template('games.html', user=session["username"])

@app.route("/superhero")
def superhero():
    """Returns Superhero Page"""
    if "userID" not in session:
        return redirect(url_for('login'))
    return render_template('superhero.html', user=session["username"])

@app.route("/anagrams")
def anagrams():
    """Returns Anagrams Page"""
    if "userID" not in session:
        return redirect(url_for('login'))
    return render_template('anagrams.html', user=session["username"])


#########################################################
#                  TRIVIA MINIGAME                      #
#########################################################

#shuffles the choices up so that the answers are not always the first choice
def shuffle(q):
    selected_keys = []
    i = 0
    while i < len(q):
        if list(q.keys())[i] not in selected_keys:
            selected_keys.append(list(q.keys())[i])
            i += 1
    return selected_keys

@app.route("/trivia")
def trivia():
    dbfunc.setup(c)
    dbfunc.addQuestions(c)
    original_questions = dbfunc.questBank(c)
    questions_shuffled = shuffle(original_questions)
    for i in original_questions.keys():
        random.shuffle(original_questions[i])
    return render_template('trivia.html', q = questions_shuffled, o = original_questions)

@app.route('/triviaresults', methods=['POST'])
def triviaresults():
    correct = 0;
    userID = session["userID"]
    original_questions = dbfunc.questBank(c)
    answers = dbfunc.answerBank(c)
    if request.method == 'POST':
        for i in original_questions.keys():
            answered = request.form[i]
            if original_questions[i][0] == answered:
                correct += 1
        original_question = {}
    else:
        return render_template('triviaresults.html', correct = correct, answers = answers)
    return render_template('triviaresults.html', correct = correct, answers = answers)

if __name__ == "__main__":
    app.debug = True
    app.run()
