import urllib.request as request
import json
import marshal

def setup(c):
    c.execute('CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY, email TEXT, username TEXT, password TEXT, displayName TEXT, image TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS schedules (scheduleID INTEGER PRIMARY KEY, schedule BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS classNames (courseCode TEXT PRIMARY KEY, className TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS groups (groupID INTEGER PRIMARY KEY, groupName TEXT, posts BLOB, members BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS posts (postIndex INTEGER PRIMARY KEY, author INTEGER, words TEXT, likers BLOB, comments BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS comments (commentIndex INTEGER PRIMARY KEY, author INTEGER, words TEXT, likers BLOB, replies BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS replies (replyIndex INTEGER PRIMARY KEY, author INTEGER, words TEXT, likers BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS leaderboards (userID INTEGER PRIMARY KEY, superheroScore INTEGER, anagramScore INTEGER, triviaScore INTEGER)')

def blobify(data):
    return marshal.dumps(data)

def unblob(stuff):
    return marshal.loads(stuff)

def countRows(c,table):
    c.execute("SELECT COUNT(*) FROM {}".format(table))
    return c.fetchall()[0][0]

#c is the cursor being used
def createUser(c, username, password, displayname, email, image):
    nextIndex = int(countRows(c,"users"))
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",(nextIndex, email, username, password, displayname, image))
    c.execute("INSERT INTO schedules VALUES(?, ?)",(nextIndex,blobify([None,None,None,None,None,None,None,None,None,None])))

def getSchedule(c,userID):
    c.execute("SELECT schedule FROM schedules WHERE scheduleID = '{}'".format(userID))
    return unblob(c.fetchall()[0][0])
