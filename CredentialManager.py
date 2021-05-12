import os
import json


def get_credentials():
    credentials_dict = {}
    exists = os.path.isfile('credentials.json')
    if exists:
        with open('credentials.json') as credentials:
            credentials_dict = json.load(credentials)
    else:
        credentials_dict['imap_server'] = input('Please enter your IMAP server: ')
        credentials_dict['username'] = input('Please enter your username: ')
        credentials_dict['password'] = input('Please enter your password: ')
        with open('credentials.json', mode='w') as f:
            f.write(json.dumps(credentials_dict))
    return credentials_dict
