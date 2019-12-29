from flask import Flask, render_template, request, g, jsonify
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

def editMessage(id, dt, author, message):
	try:
		conn = sqlite3.connect(DATABASE)
		message = (dt, author, message, id)
		sql_edit_message = """ UPDATE messages SET date = ?, author = ?, message = ? WHERE id = ? """
		cur = conn.cursor()
		cur.execute(sql_edit_message, message)
		conn.commit()
	except sqlite3.Error as er:
		print('er:', er)

def deleteMessage(id):
	try:
		conn = sqlite3.connect(DATABASE)
		message = (id,)
		sql_delete_message = """ DELETE FROM messages WHERE id = ? """
		cur = conn.cursor()
		cur.execute(sql_delete_message, message)
		conn.commit()
	except sqlite3.Error as er:
		print('er:', er)

def insertNickname(name):
	try:
		conn = sqlite3.connect(DATABASE)
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
	return render_template("index.html")

@app.route("/get-messages")
def getMessages():
	cur = get_db().cursor()
	data = cur.execute("select * from messages")
	messages = cur.fetchall()
	return jsonify(messages)

@app.route("/get-nicknames")
def getNicknames():
	cur = get_db().cursor()
	data = cur.execute("select * from nicknames")
	nicknames = cur.fetchall()
	return jsonify(nicknames)

@app.route("/submit-message", methods=['POST'])
def submitMessage():
	author = request.form.get('author')
	message = request.form['message']
	dt = str(datetime.datetime.now())
	insertMessage(message, dt, author)
	return 'OK'

@app.route("/edit-message", methods=['POST'])
def editMessageRoute():
	id = request.form['id']
	message = request.form['message']
	author = request.form['author']
	dt = str(datetime.datetime.now())
	editMessage(id, dt, author, message)
	return 'OK'

@app.route("/delete-message", methods=['POST'])
def deleteMessageRoute():
	id = request.form['id']
	deleteMessage(id)
	return 'OK'

@app.route("/add-nickname", methods=['POST'])
def addNickname():
	nickname = request.form['author']
	insertNickname(nickname)
	return 'OK'

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

if __name__ == "__main__":
    app.run()
