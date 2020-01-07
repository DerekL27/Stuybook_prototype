import urllib.request as request
import json

def setup(c):
    c.execute('CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, username TEXT, password TEXT, displayname TEXT)')

def createUser(c, username, password, displayname, email):
    c.execute("INSERT INTO users VALUES (NULL, '%s', '%s', '%s', '%s')" % (email, username, password, displayname))
