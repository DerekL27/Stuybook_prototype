from flask import Flask, render_template, request, redirect, url_for, session
import urllib.request as urlrequest
import json
import sqlite3, os
import random, string
from utl.dbfunc import setup, createUser, getSchedule, update_user, getAllPosts, addPost, updateSchedule, getAllLeaderboard, convert, unblob
from utl.dbfunc import findGroups, updateTriviaScore, addReminder, getReminders, removeReminder, createGroup, addtoGroup, removefromGroup
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
    addReminder(c, session['userID'], "Make friends on StuyBook!")
    db.commit()
    #print(getReminders(c, session["userID"]))
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
    posts = getAllPosts(c)
    authors = []
    #print(posts)
    for i in range(len(posts)):
        c.execute("SELECT displayName FROM users WHERE userID = ?",(posts[i][1],))
        authors.append(c.fetchall()[0][0])
    posts.reverse()
    authors.reverse()
    print(authors)
    return render_template('home.html', user=session["username"], posts=posts, authors=authors)

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
    c.execute("SELECT username, displayName, image, email, bio FROM users WHERE userID = '{}'".format(session['userID']))
    bruh = c.fetchone()
    schedule = getSchedule(c, session["userID"])
    remlist = getReminders(c, session["userID"])
    #print(remlist)
    return render_template('profile.html', username = bruh[0],
                                           displayName = bruh[1],
                                           schedule = schedule,
                                           image = bruh[2],
                                           email = bruh[3],
                                           bio = bruh[4], message=message, reminders=remlist)

@app.route("/update_schedule", methods=["POST"])
def schedule():
    if "userID" not in session:
        return redirect(url_for('login'))
    newschedule = []
    for i in range(0,10):
        currentperiod = request.form["period"+str(i+1)];
        oldschedule = getSchedule(c, session["userID"])
        if currentperiod == "":
            newschedule += [oldschedule[i]]
        else:
            newschedule += [currentperiod]
    regroup(c,session["userID"], newschedule)
    updateSchedule(c,session["userID"],newschedule)
    return redirect('/myprofile')

@app.route("/changePic", methods=["POST"])
def changePic():
    picUrl = request.form['newImage']
    c.execute("UPDATE users SET image = ? WHERE userID = ?",(picUrl,session['userID']))
    return redirect("/myprofile")

@app.route("/edit_bio", methods=["POST"])
def bio():
    if "userID" not in session:
        return redirect(url_for('login'))
    c.execute("UPDATE users SET bio = '%s' WHERE username = '%s'" % (request.form["newbio"], session["username"]))
    return redirect(url_for('profile'))

@app.route("/mygroups")
def mygroups():
    """Returns Home Page"""
    if "userID" not in session:
        return redirect(url_for('login'))
    groups = findGroups(c, session["userID"])
    return render_template('mygroups.html', user=session["username"], groups = convert(c, groups))

@app.route("/create-group", methods=["POST"])
def creategroup():
    if "userID" not in session:
        return redirect(url_for('login'))
    c.execute("SELECT groupID FROM groups WHERE groupName = '%s'" % request.form['groupname'])
    a = c.fetchone()
    if a != None:
        return render_template('mygroups.html', user=session["username"], groups = groups,
                                                message="Group Already Exists")
    createGroup(c, request.form['groupname'], session["userID"])
    return redirect(url_for('mygroups'))

@app.route("/groups")
def groups():
    if "userID" not in session:
        return redirect(url_for('login'))
    c.execute("SELECT groupName FROM groups")
    a = c.fetchall()
    print(a)
    return render_template('groups.html', groups=a)

@app.route("/joingroup", methods=["POST"])
def joingroup():
    if "userID" not in session:
        return redirect(url_for('login'))
    c.execute("SELECT members FROM groups WHERE groupName = '%s'" % request.form['whichgroup'])
    list = c.fetchall()[0][0]
    list = unblob(list)
    if session['userID'] in list:
        c.execute("SELECT groupName FROM groups")
        a = c.fetchall()
        return render_template('groups.html', groups=a, message="You're already in this group!")
    addtoGroup(c, request.form['whichgroup'], session["userID"])
    return redirect(url_for('login'))

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
    if (request.form['displaychange'] != ''):
        update_user(session['username'], "displayName", request.form['displaychange'])
        return render_template('settings.html', changed3=True)
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

@app.route("/reminder", methods=["POST"])
def reminder():
    if 'userID' not in session:
        redirect(url_for("login"))
    print(request.form['rem']+"!")
    if request.form['rem'] != "":
        addReminder(c, session['userID'], request.form['rem'])
        print("HERE")
        print(getReminders(c, session["userID"]))
        db.commit()
        return redirect(url_for("profile"))
    return redirect(url_for("profile"))

@app.route("/deleterem", methods=["POST"])
def deletereminder():
    if 'userID' not in session:
        redirect(url_for("login"))
    removeReminder(c, session['userID'], request.form['node'])
    return redirect(url_for("profile"))

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

@app.route("/anagrams")
def anagrams():
    """Returns Anagrams Page"""
    if "userID" not in session:
        return redirect(url_for('login'))
    str = dbfunc.randomLetters()
    print(str)
    split = [char for char in str]
    print(split)
    print(dbfunc.printWords(str))
    return render_template('anagrams.html', user=session["username"], q = split)

@app.route("/anagramsresults", methods=["POST"])
def anagramsresults():
    if 'userID' not in session:
        redirect(url_for("login"))
    input = request.form['input']
    dic = request.form['original']
    list = dbfunc.printWords(dic)
    print(input)
    if (dbfunc.checkAnagrams(dic)):
        dbfunc.updateAnagramsScore(c,userID,len(input)*1)
    return render_template('anagramsresults.html', input = input, q = list, point = len(input)*1)

@app.route("/posting", methods=["POST"])
def posting():
    if(len(request.form['body'].rstrip()) == 0):
        flash("Body has no text!")
        return redirect('/home')
    else:
        words = request.form['body']
        words = words.replace(" ","`AGDEIlGEdzgzXEN`")
        thing = urlrequest.urlopen("https://www.purgomalum.com/service/json?text={}".format(words))
        thing2 = thing.read()
        thing3 = json.loads(thing2)
        thing4 = thing3['result'].replace("`AGDEIlGEdzgzXEN`"," ")
        addPost(session['userID'],thing4)
        return redirect('/home')


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
        updateTriviaScore(c,userID,correct)
        return render_template('triviaresults.html', correct = correct, answers = answers)
    updateTriviaScore(c,userID,correct)
    return render_template('triviaresults.html', correct = correct, answers = answers)

@app.route('/leaderboard')
def leaderboard():
    if "userID" not in session:
        return redirect(url_for('login'))
    stuff = getAllLeaderboard(c)
    c.execute("SELECT displayName FROM users")
    names = c.fetchall()
    print(stuff)
    print(names)
    return render_template('leaderboard.html', stuff = stuff, names = names)


if __name__ == "__main__":
    app.debug = True
    app.run()
