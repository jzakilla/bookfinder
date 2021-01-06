-- get rid of any pre-existing table named bookshelf
DROP TABLE IF EXISTS bookshelf;
DROP TABLE IF EXISTS users;

-- create the table named bookshelf with the following SQL fields and parameters
CREATE TABLE bookshelf (
	isbn TEXT PRIMARYKEY NOT NULL,
	author TEXT NOT NULL,
	title TEXT NOT NULL,
	page_count INTEGER,
	book_format TEXT,
	genre TEXT,
	summary TEXT,
	stock INTEGER
	);

CREATE TABLE users (
	username TEXT PRIMARYKEY NOT NULL,
	password TEXT NOT NULL
	);