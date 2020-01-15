import urllib.request as request
import json
import marshal
import sqlite3

DB_FILE = "database.db"

def setup(c):
    c.execute('CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY, email TEXT, username TEXT, password TEXT, displayName TEXT, image TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS schedules (scheduleID INTEGER PRIMARY KEY, schedule BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS classNames (courseCode TEXT PRIMARY KEY, className TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS groups (groupID INTEGER PRIMARY KEY, groupName TEXT, posts BLOB, members BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS posts (postIndex INTEGER PRIMARY KEY, author INTEGER, words TEXT, likers BLOB, comments BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS comments (commentIndex INTEGER PRIMARY KEY, author INTEGER, words TEXT, likers BLOB, replies BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS replies (replyIndex INTEGER PRIMARY KEY, author INTEGER, words TEXT, likers BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS leaderboards (userID INTEGER PRIMARY KEY, superheroScore INTEGER, anagramScore INTEGER, triviaScore INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS trivia (number INTEGER, questions TEXT, one TEXT, two TEXT, three TEXT, four TEXT)')

def update_user(username, field, newvalue):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("UPDATE users SET %s = '%s' WHERE username = '%s'" % (
                field,
                newvalue,
                username
            )
        )
    db.commit()
    c.close()
    return "Success"

def placeholderName(userID):
    nextIndex = int(countRows(c,"groups"))
    groupsIn = [] #all the groups user is in
    groupsInfo = [] #basically SELECT * FROM groups WHERE (user is a member of)
    for i in range(nextIndex):
        c.execute("SELECT members FROM groups WHERE groupID = {}".format(nextIndex))
        if(userID in unblob(c.fetchall()[0][0])):
            groupsIn.append(i)
    for i in groupsIn:
        c.execute("SELECT * FROM groups WHERE groupID = {}".format(i))
        groupsInfo.append(c.fetchall()[0])
    return groupsInfo

def blobify(data):
    return marshal.dumps(data)

def unblob(stuff):
    return marshal.loads(stuff)

def getAllPosts(c):
    c.execute("SELECT * FROM posts")
    a = c.fetchall()
    return a

def getAllLeaderboard(c):
    c.execute("SELECT * FROM leaderboards")
    a = c.fetchall()
    return a

def updateTriviaScore(userID,score): #where score is how many they got right on the most recent trivia thing
    c.execute("SELECT triviaScore FROM leaderboards WHERE userID = '{}'".format(userID))
    asdf = c.fetchall()[0][0]
    c.execute("UPDATE leaderboards SET triviaScore = {} WHERE userID = {}".format(asdf+score,userID))

def countRows(c,table):
    c.execute("SELECT COUNT(*) FROM {}".format(table))
    return c.fetchall()[0][0]

def addPost(userID,text):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    nextIndex = int(countRows(c,"posts"))
    c.execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?)",(nextIndex,userID,text,blobify([]),blobify([])))
    db.commit()

#c is the cursor being used
def createUser(c, username, password, displayname, email, image):
    nextIndex = int(countRows(c,"users"))
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",(nextIndex, email, username, password, displayname, image))
    c.execute("INSERT INTO schedules VALUES(?, ?)",(nextIndex,blobify([None,None,None,None,None,None,None,None,None,None])))
    c.execute("INSERT INTO leaderboards VALUES (?, ?, ?, ?)",(nextIndex,0,0,0))

def createGroup(c,groupName,userID):
    nextIndex = int(countRows(c,"groups"))
    c.execute("INSERT INTO groups VALUES (?, ?, ?, ?)",(nextIndex,groupName,blobify([]),blobify([userID])))

def addtoGroup(c,groupID,userID):
    c.execute("SELECT members FROM groups WHERE groupID = {}".format(groupID))
    list = c.fetchall()[0][0]
    list = unblob(list)
    list.append(userID)
    list = blobify(list)
    c.execute("UPDATE groups SET members = ? WHERE groupID = ?",(list,groupID))

def getSchedule(c,userID):
    c.execute("SELECT schedule FROM schedules WHERE scheduleID = '{}'".format(userID))
    return unblob(c.fetchall()[0][0])

def updateSchedule(c,userID,newschedule):
    print("hello!!")
    c.execute("UPDATE schedules SET schedule = ? WHERE scheduleID = ?",(blobify(newschedule),userID))

def quest(bank):
    """Makes dictionary from Open Trivia API"""
    q = request.urlopen("https://opentdb.com/api.php?amount=10&category=18&type=multiple").read()
    for i in range(5):
        count = json.loads(q)['results'][i]
        ans = [count['correct_answer']]
        bank[count['question']] = [*ans,*count['incorrect_answers']]
    return bank

def addQuestions(c):
    """Adds questions and choices into the database"""
    og = {}
    og = quest(og)
    for i in range(5):
        ques = list(og)[i]
        c.execute('INSERT INTO trivia VALUES (?, ?, ?, ?, ?, ?)', (i, ques, og[ques][0], og[ques][1], og[ques][2], og[ques][3]))

def getQuestion(c, i):
    """Get the question given the index"""
    return c.execute("SELECT questions, one, two, three, four FROM trivia WHERE number = ?", (i, )).fetchone()

def questBank(c):
    """Returns the dictionary from the stored information"""
    bank = []
    for i in range(5):
        bank.append(getQuestion(c, i))
    bankDic = {}
    for i in range(5):
        bankDic[bank[i][0]] = [bank[i][1], bank[i][2], bank[i][3], bank[i][4]]
    return bankDic

def answerBank(c):
    """Returns the dictionary with the question : [answer]"""
    bank = []
    for i in range(5):
        bank.append(getQuestion(c, i))
    bankDic = {}
    for i in range(5):
        bankDic[bank[i][0]] = [bank[i][1]]
    return bankDic
