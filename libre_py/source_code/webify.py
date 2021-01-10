from flask import Flask, render_template, request, url_for, flash, redirect
import pymongo
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
import string, random


# db functions go here
# build and return connector
def get_db_connection():
	myclient = pymongo.MongoClient()
	db = myclient.librarydb
	return db


def book_check(ISBN):
	db = get_db_connection()
	bookshelf = db.bookshelf

	result = bookshelf.find_one({"isbn": ISBN})

	if result == None:
		result = 'False'
	else:
		result = 'True'
	
	return result


pool = string.ascii_lowercase + string.ascii_uppercase + string.digits
length = 16
random_key = ''.join(random.choice(pool) for _ in range(length))

# intialize flask app
app = Flask(__name__)
# Secret key is necessary to render pages properly between page navigation
app.config['SECRET_KEY'] = random_key


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/browse')
def browse():
	db = get_db_connection()
	bookshelf = db.bookshelf
	for book in bookshelf.find():
		print(book)
	book_count = db.bookshelf.count()
	return render_template('browse.html', book_count=book_count)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		user = request.form['username']
		password = request.form['password']
		email = request.form['email']
		address = request.form['address']
		bus_name = request.form['business_name']
		phone = request.form['phone']

		hashed = generate_password_hash(password, method='sha256', salt_length=8)
		db = get_db_connection()
		users = db.users

		new_user = {"user": user, "password": hashed, "email": email, "address": address, "bus_name":bus_name, "phone": phone}

		users.insert_one(new_user)
	return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		passw = request.form['password']
		user = request.form['username']
		# find username in database
		db = get_db_connection()
		users = db.users

		result = users.find_one({"user": user})

		if result == None:
		 	return redirect(url_for('signup'))
		else:
		# check password hash against hash password
			tocheck = result['password']
			pwd_check = check_password_hash(tocheck, passw)
			
			# check hashed password against supplied password
			if pwd_check == True:
			 	return redirect(url_for('stocking'))
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
			db = get_db_connection()
			bookshelf = db.bookshelf

			new_book = {"title": title, "author": author, "isbn": isbn, "page_count": page_count, "book_format": book_format, "genre": genre, "summary": summary, "stock": 1}
			bookshelf.insert_one(new_book)
			flash('{} successfully enrolled'.format(title))

	return render_template('enrollment.html')


@app.route('/stocking', methods=['GET', 'POST'])
def stocking():
	if request.method == 'POST':
		ISBN = request.form['barcode_input'].replace("-", "")
		db = get_db_connection()
		bookshelf = db.bookshelf
		
		exists = bookshelf.find_one({"isbn": ISBN})
		
		# increment or decrement?
		decision = request.form.get('inv_management')
		# does it exist in the database?
		if exists == None:
			return redirect(url_for('enrollment'))
		
		# increment if it exists and increment is called for
		if (exists['stock'] > 0) and (decision == "stock"):
			count = int(exists['stock']) + 1
			print("updated count is {}".format(count))
			bookshelf.update_one(
				{'isbn': ISBN},
				{
					"$set": {"stock": count}
				})
			
			print("Book quantity increased by one")
		elif (exists['stock'] > 0) and (decision == "sell"):
			count = int(exists['stock']) - 1
			bookshelf.update_one(
				{'isbn': ISBN},
				{
					"$set": {"stock": count}
				})
			
			print("Book quantity reduced by one")
		elif (exists['stock'] == 0) and (decision == "sell"):
			bookshelf.delete_one({"isbn": ISBN})
			
			print("Book no longer exists")


	return render_template('stocking.html')


# need lookup method definition here, to be called by query
@app.route('/results', methods=['GET', 'POST'])
def results():
	user_choice = request.form.get('user_choice')
	user_input = request.form.get('user_input')
	db = get_db_connection()
	bookshelf = db.bookshelf


	if user_choice == 'isbn':
		user_input = user_input.replace("-", "")
		result = bookshelf.find({"isbn": user_input})
	elif user_choice == 'author':
		result = bookshelf.find({"author": user_input})
	elif user_choice == 'title':
		result = bookshelf.find({"author": user_input})

	books = []

	if result == None:
		return redirect(url_for('enrollment'))
	else:
		for item in result:
			books.append(item)
		return render_template('results.html', books=books)


if __name__ == '__main__':
	app.run(host="0.0.0.0")