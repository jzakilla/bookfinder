from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash


# db functions go here
# build and return connector
def get_db_connection():
	conn = sqlite3.connect('library.db')
	conn.row_factory = sqlite3.Row
	return conn


# query db for book, return results
def get_books(qtype, qstring):
	conn = get_db_connection()
	
	if qtype == 'isbn':
		books = conn.execute('SELECT * FROM bookshelf WHERE isbn = ?', (qstring,)).fetchall()
	elif qtype == 'author':
		books = conn.execute('SELECT * FROM bookshelf WHERE author LIKE ?', ('%'+qstring+'%',)).fetchall()
	elif qtype == 'title':
		books = conn.execute('SELECT * FROM bookshelf WHERE title LIKE ?', ('%'+qstring+'%',)).fetchall()

	conn.close()
	return books
	

def book_check(ISBN):
	conn = get_db_connection()
	count = conn.execute('SELECT * FROM bookshelf WHERE isbn = ?', (ISBN,))
	result_dict = dict(count.fetchone())
	if len(result_dict) > 0:
		result = 'True'
	else:
		result = 'False'
	conn.close()
	return result

# intialize flask app
app = Flask(__name__)
# Secret key is necessary to render pages properly between page navigation
app.config['SECRET_KEY'] = 'helpthechildrenreadmore'


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/browse')
def browse():
	conn = get_db_connection()
	books = conn.execute('SELECT * FROM bookshelf').fetchall()
	book_count = len(list(books))
	conn.close()
	return render_template('browse.html', book_count=book_count)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		address = request.form['address']
		bus_name = request.form['business_name']
		phone = request.form['phone']

		hashed = generate_password_hash(password, method='sha256', salt_length=8)
		conn = get_db_connection()
		conn.execute('INSERT INTO users (username, password, email, address, business_name, phone) VALUES (?, ?, ?, ?, ?, ?)',
		 (username, hashed, email, address, bus_name, phone))
		conn.commit()
		conn.close()
	return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		passw = request.form['password']
		user = request.form['username']
		# find username in database
		conn = get_db_connection()
		cur = conn.cursor()

		user_entry = cur.execute('SELECT * FROM users WHERE username = ?', (user,))
		# result = [dict(row) for row in cur.fetchall()]
		result = [dict(row) for row in user_entry]
		# print(result[0]['password'])
		
		if len(result) == 0:
			return redirect(url_for('signup'))
		else:
			# check password hash against hash password
			print(result[0]['password'])
			print(passw)
			print(generate_password_hash(passw, method='sha256', salt_length=8))
			pwd_check = check_password_hash(result[0]['password'], passw)
			
			# check hashed password against supplied password
			if pwd_check == 'True':
				print("Good to go")
			else:
				print("Didn't pass")
			# direct user / flash message
	return render_template('login.html')


# Enrollment page for books that aren't found
@app.route('/enrollment', methods=('GET', 'POST',))
def enrollment():
	if request.method == 'POST':
		title = request.form['title']
		author = request.form['author']
		isbn = request.form['isbn'].replace("-", "")
		page_count = request.form['page_count']
		book_format = request.form['book_format']
		genre = request.form['genre']
		summary = request.form['summary']

		if not isbn:
			flash('ISBN is required!')
		elif book_check(isbn) == 'True':
			flash('ISBN already exists in database')
		else:
			conn = get_db_connection()
			conn.execute('INSERT INTO bookshelf (isbn, author, title, page_count, book_format, genre, summary, stock) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
		 (isbn, author, title, page_count, book_format, genre, summary, 1))
			conn.commit()
			conn.close()
			flash('{} successfully enrolled'.format(title))

	return render_template('enrollment.html')


@app.route('/stocking', methods=['GET', 'POST'])
def stocking():
	if request.method == 'POST':
		ISBN = request.form['barcode_input'].replace("-", "")
		conn = get_db_connection()
		count = conn.execute('SELECT * FROM bookshelf WHERE isbn = ?', (ISBN,))
		results = dict(count.fetchone())
		# increment or decrement?
		decision = request.form.get('inv_management')
		# does it exist in the database?
		if len(results) == 0:
			return redirect(url_for('enrollment'))
		
		# increment if it exists and increment is called for
		if (results['stock'] > 0) and (decision == "stock"):
			conn.execute('UPDATE bookshelf SET stock = stock + 1 WHERE isbn = ?', (ISBN,))
			conn.commit()
			print("Book quantity increased by one")
		elif (results['stock'] >= 1) and (decision == "sell"):
			conn.execute('UPDATE bookshelf SET stock = stock - 1 WHERE isbn = ?', (ISBN,))
			conn.commit()
			print("Book quantity reduced by one")
		elif (results['stock'] == 0) and (decision == "sell"):
			conn.execute('DELETE FROM bookshelf WHERE isbn = ?', (ISBN,))
			conn.commit()
			print("Book no longer exists")

		conn.close()

	return render_template('stocking.html')


# need lookup method definition here, to be called by query
@app.route('/results', methods=['GET', 'POST'])
def results():
	user_choice = request.form.get('user_choice')
	user_input = request.form.get('user_input')

	if user_choice == 'isbn':
		user_input = user_input.replace("-", "")
		books = get_books('isbn', user_input)
	elif user_choice == 'author':
		books = get_books('author', user_input)
	elif user_choice == 'title':
		books = get_books('title', user_input)

	if (len(books) == 0):
		return redirect(url_for('enrollment'))
	else:
		return render_template('results.html', books=books)
