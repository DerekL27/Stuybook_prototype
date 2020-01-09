import urllib.request as request
import json

def setup(c):
    c.execute('CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY, email TEXT, username TEXT, password TEXT, displayName TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS schedules (scheduleID INTEGER PRIMARY KEY, schedule BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS groups (groupID INTEGER PRIMARY KEY, groupName TEXT, posts BLOB, members BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS posts (postIndex INTEGER PRIMARY KEY, author INTEGER, words TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS leaderboards (userID INTEGER PRIMARY KEY, superheroScore INTEGER, anagramScore INTEGER, triviaScore INTEGER)')

def countRows(table):
    c.execute("SELECT COUNT(*) FROM {}".format(table))
    return c.fetchall()[0]

#c is the cursor being used
def createUser(c, username, password, displayname, email):
    nextIndex = countRows("users")
    c.execute("INSERT INTO userdata VALUES (?, ?, ?, ?, ?)",(nextIndex, email, username, password, displayname))
    c.execute("INSERT INTO schedules VALUES(?, ?),(nextIndex,[null,null,null,null,null,null,null,null,null,null]) ")
