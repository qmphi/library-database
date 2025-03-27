import sqlite3

database = 'library.db'

sql_statements = ['''
CREATE TABLE IF NOT EXISTS item (
    itemID INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    publicationYear INTEGER,
    genre TEXT,
    itemType TEXT,
    isAvailable INTEGER CHECK(isAvailable IN (0, 1)),
    location TEXT
);
'''
]
try:
    with sqlite3.connect(database) as conn:

        cursor = conn.cursor()

        for statement in sql_statements:
            cursor.execute(statement)

        conn.commit()

        print("Tables Created!")
except sqlite3.OperationalError as e:
    print(e)