import urllib.request as request
import json

def setup(c):
    c.execute('CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, username TEXT, password TEXT, displayName TEXT, scheduleIndex INTEGER FOREIGN KEY)')
    c.execute('CREATE TABLE IF NOT EXISTS schedules (index INTEGER PRIMARY KEY, schedule BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS groups (index INTEGER PRIMARY KEY, groupName TEXT, posts BLOB, members BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS posts (postIndex INTEGER PRIMARY KEY, author INTEGER, words TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS leaderboards (userID INTEGER PRIMARY KEY, superheroScore INTEGER, anagramScore INTEGER, triviaScore INTEGER)')

def createUser(c, username, password, displayname, email):
    c.execute("INSERT INTO users VALUES(NULL, '%s', '%s', '%s', '%s')" % (email, username, password, displayname))
