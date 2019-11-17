from flask import Flask, render_template, request, g
import sqlite3
import os
import datetime

app = Flask(__name__)

DATABASE = './multi-chat.db'

def createDB():
	conn = sqlite3.connect(DATABASE)
	sql_create_messages_table = """ CREATE TABLE IF NOT EXISTS messages (
			id integer PRIMARY KEY,
			message text NOT NULL,
			date text NOT NULL,
			author text NOT NULL
		);
	"""
	conn.execute(sql_create_messages_table)

	sql_create_names_table = """ CREATE TABLE IF NOT EXISTS nicknames (
			id integer PRIMARY KEY,
			name text NOT NULL
		);
	"""
	conn.execute(sql_create_names_table)

def insertMessage(newMessage, dt, author):
	try:
		conn = sqlite3.connect(DATABASE)
		message = (newMessage, dt, author)
		sql_insert_message = """ INSERT INTO messages (message, date, author) VALUES (?, ?, ?) """
		cur = conn.cursor()
		cur.execute(sql_insert_message, message)
		conn.commit()
	except sqlite3.Error as er:
		print('er:', er)

def insertNickname(name):
	try:
		conn = sqlite3.connect(DATABASE)
		print(name)
		nickname = (name,)
		sql_insert_nickname = """ INSERT INTO nicknames (name) VALUES (?) """
		cur = conn.cursor()
		cur.execute(sql_insert_nickname, nickname)
		conn.commit()
	except sqlite3.Error as er:
		print('er:', er)

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

createDB()

@app.route("/")
def home():
	cur = get_db().cursor()
	data1 = cur.execute("select * from messages")
	messages = cur.fetchall()
	data2 = cur.execute("select * from nicknames")
	nicknames = cur.fetchall()
	return render_template("index.html", messages=messages, nicknames=nicknames)

@app.route("/submit-message", methods=['POST'])
def submitMessage():
	author = request.form['author']
	message = request.form['message']
	dt = str(datetime.datetime.now())
	insertMessage(message, dt, author)
	return 'OK'

@app.route("/add-nickname", methods=['POST'])
def addNickname():
	nickname = request.form['nickname']
	insertNickname(nickname)
	return 'OK'

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

if __name__ == "__main__":
    app.run()
