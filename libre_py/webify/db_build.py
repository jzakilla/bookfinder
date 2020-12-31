import sqlite3

connection = sqlite3.connect('library.db')
with open('schema.sql') as file:
	connection.executescript(file.read())

connection.commit()
connection.close()