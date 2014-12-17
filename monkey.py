#!/usr/bin/env python


import time
import sqlite3 as lite
import os
from http import cookies
import json

loggedIn = False

print("Monkey 1.0 is ready to fling!")

def createDB():
	conn = lite.connect('test.db')
	conn.execute('''CREATE TABLE IF NOT EXISTS USERS
				(USERNAME TEXT UNIQUE NOT NULL,
				PASSWORD TEXT NOT NULL);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS OOKS
				(USERNAME TEXT NOT NULL,
				OOK TEXT NOT NULL,
				TIME TEXT NOT NULL);''')
	conn.commit()
	conn.close()

def printRecords(self):
	createDB()
	conn = lite.connect('test.db')
	cursor = conn.execute("SELECT time, username, ook FROM OOKS ORDER BY TIME DESC")
	s = ""
	n = 0
	tmp = []

	for row in cursor:
		tmp.append({'username':row[1], 'time':row[0], 'ook':row[2]})
		#s = "<p align='left' class='ook'><span class='foo'>" + row[1] + " " + row[0] + "</span><br> " + row[2] + "</p>" + s;
		n += 1
		if n == 5:
			conn.close()
			json.dump(tmp, self.remote)
			#self.remote.write(s) 
			return

	conn.close()
	json.dump(tmp, self.remote)
	#self.remote.write(s)

def updateRecord(username, update):
	updateTime = time.strftime("%b %d %Y %H:%M:%S", time.gmtime())
	conn = lite.connect("test.db")
	conn.execute("INSERT INTO OOKS (OOK, TIME, USERNAME) VALUES (?, ?, ?)", (update, updateTime, username))
	conn.commit()
	conn.close()

def addRecord(username, password):
	updateTime = time.strftime("%b %d %Y %H:%M:%S", time.gmtime())
	conn = lite.connect("test.db")
	cursor = conn.cursor()
	cursor.execute("INSERT INTO USERS (USERNAME, PASSWORD) VALUES (?, ?)", (username, password))

	cursor.execute("INSERT INTO OOKS (USERNAME, OOK, TIME) VALUES (?, ?, ?)", (username, "I joined Ook!", updateTime))
	conn.commit()
	conn.close()

def signUp(self, user, password, email):
	if(checkUser(user) == True):
		addRecord(user, password)
		self.send_header("Set-Cookie", "username=" + user + ";")
		self.send_header("Set-Cookie", "loggedIn=True")

def login(self, user, password):
	if(checkUser(user) == False and checkPass(password) == False):
		self.send_header('Set-Cookie', 'username=' + user + ";")
		self.send_header('Set-Cookie', 'loggedIn=True')
	else:
		print("invalid password or username")

def ook(self):
	cookie = self.headers['cookie']
	if not cookie:
		return

	cookie = cookie.split(";")

	log = cookie[1].split("=")

	if log[1] == 'False':
		print('cant ook')
		return

	printOok(self)
	user = cookie[0].split("=")
	ook = self.fs.getfirst('ooks',None)
	if(ook):
		updateRecord(user[1], ook)

def logout(self):
	cookie = self.headers['cookie']

	if not cookie:
		return

	self.send_header("Set-Cookie", "username=None" + ";")
	self.send_header("Set-Cookie", "loggedIn=False")

def display(self):
	cookie = self.headers['cookie']
	if not(self.headers['cookie']):
		text(self)
		return
	cookie = cookie.split(";")
	log = cookie[1].split("=")
	logged = log[1]

	if logged == 'True':
		displayLogout(self)
	else:
		text(self)

def checkUser(username):
	conn = lite.connect('test.db')
	cursor = conn.execute("SELECT USERNAME from USERS")
	print(username)
	for row in cursor:
		if(username == row[0]):
			conn.close()
			return False

	conn.close()
	return True

def checkPass(password):
	conn = lite.connect('test.db')
	cursor = conn.execute("SELECT PASSWORD from USERS")
	for row in cursor:
		print(row)
		if(password == row[0]):
			conn.close()
			return False

	conn.close()
	return True

def displayLogout(self):
	self.remote.write('''<div class="log">''')
	self.remote.write('''<form class="pure-form pure-form-stacked" action='logout.html'>
			<fieldset class="pure-group" method='POST'>
				<legend>Log Out</legend>
				<button type='submit' name='logout' class="pure-button pure-button-primary">Logout</button>
			</fieldset>
			</form>''')
	self.remote.write('''</div>''')

def text(self):
	self.remote.write('''<div class="login">''')
	self.remote.write('''<form class="pure-form" action='login.html'>
    <fieldset class="pure-group">
        <legend>Log in!</legend>
        <input name='username' placeholder="Username">
        <input type='password' name='password' placeholder="Password">
        <button type='submit' class="pure-button pure-button-primary">Log In</button>
    </fieldset>
	</form>''')
	self.remote.write('''</div>''')
	self.remote.write('''<div class="signup">''')
	self.remote.write('''<form class="pure-form pure-form-stacked" action='signup.html'>
		<fieldset class="pure-group">
			<legend>Sign up!</legend>
			<input name='username' placeholder="Username">
			<input type='password' name='password1' placeholder="Password">
			<input name='email' placeholder="Email">
			<button type='submit' class="pure-button pure-button-primary">Sign Up</button>
		</fieldset>
		</form>''')
	self.remote.write('''</div>''')

def printOok(self):
	self.remote.write('''<form action='index.html' class="pure-form">
        <fieldset>
            <input name='ooks' maxlength=140 size=100>
            <input type='submit' class="pure-button pure-button-primary" value="OOK! OOK!">
        </fieldset>
    </form>''')