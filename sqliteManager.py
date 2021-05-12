import sqlite3
import re

DATABASE = 'kindle_quotes.db'

def connect_to_database(name):
    return sqlite3.connect(name)


def create_database():
    con = connect_to_database(DATABASE)
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS quotes
                     (ID Integer PRIMARY KEY AUTOINCREMENT NOT NULL, quote text UNIQUE, source text, Timestamp DATETIME DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW', 'localtime'))) ''')
    con.commit()
    con.close()


def write_quote_to_db(quote):
    con = connect_to_database(DATABASE)
    extracted_quote = re.findall(r'"([^"]*)"', quote)
    if len(extracted_quote) > 0:
        print("Writing quote to database")
        con.execute("INSERT OR IGNORE INTO quotes(quote, source) VALUES(?, ?)",
                    (extracted_quote[0],
                     extracted_quote[1]))
        con.commit()
        con.close()
