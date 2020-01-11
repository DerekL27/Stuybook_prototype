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
    if "userID" not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route("/myprofile")
def profile():
    """Returns profile page"""
    return "Woah!"

"""
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
    dbfunctions.createTables(c)
    dbfunctions.addQuestions(c)
    original_questions = dbfunctions.questBank(c)
    questions_shuffled = shuffle(original_questions)
    for i in original_questions.keys():
        random.shuffle(original_questions[i])
    return render_template('trivia.html', q = questions_shuffled, o = original_questions)

@app.route('/triviaresults', methods=['POST'])
def triviaresults():
    correct = 0;
    userID = session['userID']
    original_questions = dbfunctions.questBank(c)
    answers = dbfunctions.answerBank(c)
    if request.method == 'POST':
        for i in original_questions.keys():
            answered = request.form[i]
            if original_questions[i][0] == answered:
                correct += 1
        original_question = {}
    else:
        return render_template('triviaresults.html', correct = correct, answers = answers)
    dbfunctions.updateStats(c, userID, intelligence = (correct * 3), xp = (correct * 5), gold = (correct * 2)) # each question correct is +3 to intelligence
    stats = dbfunctions.getStats(c, str(userID))
    currXP = stats['xp']
    leveledUp = dbfunctions.levelUp(currXP-(5 * correct), currXP)
    return render_template('triviaresults.html', correct = correct, answers = answers, intelligence = stats['intelligence'], xp = currXP, leveledUp = leveledUp, gold = (correct * 2))
"""

if __name__ == "__main__":
    app.debug = True
    app.run()
