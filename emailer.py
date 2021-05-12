# -*- coding: utf-8 -*-
import imaplib
import email
import email.parser
from email.header import decode_header
from email import policy
import re
import json
import sqlite3
import quopri
import CredentialManager

DATABASE = 'kindle_quotes.db'


def connect_to_database(name):
    return sqlite3.connect(name)


def create_database():
    con = connect_to_database(DATABASE)
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS quotes
                     (quote text, source text, PRIMARY KEY("quote")) ''')
    con.commit()
    con.close()


def write_quote_to_db(quote):
    con = connect_to_database(DATABASE)
    extracted_quote = re.findall(r'"([^"]*)"', quote)
    if len(extracted_quote) > 0:
        print("Writing quote to database")
        con.execute("INSERT OR IGNORE INTO quotes VALUES(?, ?)",
                    (extracted_quote[0],
                     extracted_quote[1]))
        con.commit()
        con.close()


def get_email():
    credentials_dict = CredentialManager.get_credentials()
    with open('credentials.json') as credentials:
        credentials_dict = json.load(credentials)
        server = credentials_dict['imap_server']
        username = credentials_dict['username']
        password = credentials_dict['password']

    imap_host = server
    imap_user = username
    imap_pass = password
    imap = imaplib.IMAP4_SSL(imap_host)

# login to server
    imap.login(imap_user, imap_pass)

    imap.select('Inbox')

    quote = ''
    tmp, data = imap.search(None, 'ALL')
    for num in data[0].split():
        tmp, data = imap.fetch(num, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                email_parser = email.parser.BytesFeedParser(policy=policy.default)
                email_parser.feed(response_part[1])
                msg = email_parser.close()
                if 'no-reply@amazon.com' in msg['from'] and 'Zitat' in msg['subject']:
                    if msg.is_multipart():
                        for payload in msg.get_payload():
                            # if payload.is_multipart(): ...
                            quote = payload.get_payload()
                write_quote_to_db(quopri.decodestring(quote).decode('utf-8'))
    imap.close()


def main():
    create_database()
    get_email()


if __name__ == "__main__":
    main()
