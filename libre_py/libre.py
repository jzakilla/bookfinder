#!/usr/bin/python3

import tkinter as tk
from tinydb import TinyDB, Query, where

db = TinyDB('./library.json')

# sanity checks: do the config and library files exist. If not, create them


# class definitions
class Book():
	# use **kwargs to build this maybe?
	def __init__(self):
		self.isbn = ''
		self.title = ''
		self.author = ''
		self.pub_date = ''
		self.format = ''
		self.length = ''
		self.barcode = ''
		self.publisher = ''
		self.genre = ''

	def enroll_book(self):
		db.insert(self.__dict__)

	def book_info(self, barcode):
		book_stats = db.get(Query()['barcode'] == barcode)
		self.title = book_stats.get('title')
		self.author = book_stats.get('author')
		self.format = book_stats.get('format')
		self.pub_date = book_stats.get('pub_date')
		self.publisher = book_stats.get('publisher')
		self.length = book_stats.get('length')
		print("You have scanned {} by {} in {} format.".format(self.title, self.author, self.format))
		print("Book published {} by {}, with a length of {} pages.".format(self.pub_date, self.publisher, self.length))


# check if book is in DB
def book_check(barcode):
	results = False
	#code to lookup in database, set results to True / False
	barcode_of_interest = Query()
	db_result = db.search(barcode_of_interest.barcode == barcode)
	if (db_result):
		results = True
	else:
		results = False
	return results


def main():
	# scan barcode and create BookCheck object
	barcode = input("Scan a barcode, or manually enter ISBN: ")
	# use book_check function to check if book ISBN is registered in database
	book_status = book_check(barcode)
	# if yes, do nothing if no, ask for user input
	if (book_status == True):
		pre_existing_book = Book()
		pre_existing_book.book_info(barcode)
	else:
		# ask user questions, create book object, and enroll in database
		isbn = input("Please enter the book's ISBN ")
		title = input("What is the book's title? ")
		author = input("Who is the book's author? ")
		publisher = input("Who publishes this book? ")
		pub_date = input("What is the date of publication (MM/DD/YYYY)? ")
		genre = input("What genre is this book? ")
		bformat = input("What format is this book in (paperback, hardcover, etc.)? ")
		length = input("How many pages is this book? ")

		new_book = Book()
		new_book.length = length
		new_book.title = title
		new_book.pub_date = pub_date
		new_book.author = author
		new_book.format = bformat
		new_book.barcode = barcode
		new_book.isbn = isbn
		new_book.publisher = publisher
		new_book.genre = genre

		new_book.enroll_book()


if __name__ == '__main__':
	main()
