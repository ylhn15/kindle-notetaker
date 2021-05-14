# -*- coding: utf-8 -*-
import imaplib
import email
import email.parser
from email import policy
import json
import quopri
import time
import CredentialManager
import sqliteManager
import firebaseManager

DATABASE = 'kindle_quotes.db'


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
                if 'no-reply@amazon.com' in msg['from'] or 'kindle-quote' in msg['subject']:
                    if msg.is_multipart():
                        for payload in msg.get_payload():
                            quote = payload.get_payload()
                # sqliteManager.write_quote_to_db(quopri.decodestring(quote).decode('utf-8'))
                firebaseManager.write_quote_to_db(quopri.decodestring(quote).decode('utf-8'))
                imap.store(num, '+FLAGS', '\\Deleted')
                imap.expunge()
    imap.close()


def main():
    sqliteManager.create_database()
    while True:
        get_email()
        time.sleep(60)


if __name__ == '__main__':
    main()
