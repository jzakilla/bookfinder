# import module needed for sqlite3
import sqlite3

# create connection object needed to operate on db
connection = sqlite3.connect('library.db')
# open file named schema.sql
with open('schema.sql') as file:
	# use connection object to create db / table as described in schema.sql
	connection.executescript(file.read())

# commit our changes to the database
connection.commit()
# close the connection
connection.close()