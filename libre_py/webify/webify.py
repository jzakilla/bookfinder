from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort


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


	return books
	conn.close()


# intialize flask app
app = Flask(__name__)
# Secret key is necessary to render pages properly between page navigation
app.config['SECRET_KEY'] = 'helpthechildrenreadmore'


@app.route('/')
def index():
	conn = get_db_connection()
	books = conn.execute('SELECT * FROM bookshelf').fetchall()
	book_count = len(list(books))
	conn.close()
	return render_template('index.html', book_count=book_count)


# success page


# enrollment. At end of enrollment, check if ISBN exists in database.
# if it does not, allow the book to be enrolled, othwise return page for that book.
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
		else:
			conn = get_db_connection()
			conn.execute('INSERT INTO bookshelf (isbn, author, title, page_count, book_format, genre, summary) VALUES (?, ?, ?, ?, ?, ?, ?)',
		 (isbn, author, title, page_count, book_format, genre, summary))
			conn.commit()
			conn.close()
			flash('{} successfully enrolled'.format(title))

	return render_template('enrollment.html')


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