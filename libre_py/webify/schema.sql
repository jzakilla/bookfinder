DROP TABLE IF EXISTS bookshelf;

CREATE TABLE bookshelf (
	isbn TEXT PRIMARYKEY NOT NULL,
	author TEXT NOT NULL,
	title TEXT NOT NULL,
	page_count INTEGER,
	book_format TEXT,
	genre TEXT,
	summary TEXT
	);