import sqlite3

CREATE_COMICS_TABLE = """CREATE TABLE IF NOT EXISTS comics (
    id INTEGER PRIMARY KEY,
    series TEXT,
    volume INTEGER,
    number INTEGER,
    publisher TEXT,
    writer TEXT,
    penciller TEXT,
    letterer TEXT,
    colorist TEXT,
    inker TEXT,
    editor TEXT
)"""

CREATE_TRADES_TABLE = """CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY,
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

INSERT_COMIC = """INSERT INTO comics (series, volume, number, publisher, writer, penciller, letterer, colorist, inker, editor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

INSERT_TRADE =  """INSERT INTO trades (title, publisher, issues, writers, pencillers, letterers, colorists, inkers, editors) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

SELECT_ALL_COMICS = "SELECT * FROM comics"

connection = sqlite3.connect("comics.db")

def create_tables():
    with connection:
        connection.execute(CREATE_COMICS_TABLE)
        connection.execute(CREATE_TRADES_TABLE)

def add_comic(comic):
    with connection:
        connection.execute(INSERT_COMIC, (comic.series, comic.volume, comic.number, comic.publisher, comic.writer, comic.penciller, comic.letterer, comic.colorist, comic.letterer, comic.editor))

def add_trade(trade):
    with connection:
        connection.execute(INSERT_TRADE, (trade.name, trade.publisher, trade.issues, 
                                  trade.writers, trade.pencillers, trade.inkers,
                                  trade.colorists, trade.letterers, trade.editors))
def get_comics():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL_COMICS)
        return cursor.fetchall()