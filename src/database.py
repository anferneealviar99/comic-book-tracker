import sqlite3

CREATE_COMICS_TABLE = """CREATE TABLE IF NOT EXISTS comics (
    title TEXT,
    publisher TEXT,
    writer TEXT,
    penciller TEXT,
    letterer TEXT,
    colorist TEXT,
    inker TEXT,
    editor TEXT
)"""

CREATE_TRADES_TABLE = """CREATE TABLE IF NOT EXISTS trades (
    title TEXT,
    publisher TEXT,
    issues TEXT,
    writers TEXT,
    pencillers TEXT,
    letterers TEXT,
    colorists TEXT,
    inkers TEXT,
    editors TEXT
)"""

CREATE_READING_LIST_TABLE = """CREATE TABLE IF NOT EXISTS read (
    reader TEXT,
    title TEXT,
    rating INTEGER,
    review TEXT,
)"""

INSERT_COMIC = """INSERT INTO comics (title, publisher, writer, penciller, letterer, colorist, inker, editor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

SELECT_ALL_COMICS = "SELECT * FROM comics"

connection = sqlite3.connect("comics.db")

def create_tables():
    with connection:
        connection.execute(CREATE_COMICS_TABLE)

def add_comic(comic):
    with connection:
        connection.execute(INSERT_COMIC, (comic.name, comic.publisher, comic.writer, comic.penciller, comic.letterer, comic.colorist, comic.letterer, comic.editor))

def get_comics():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL_COMICS)
        return cursor.fetchall()