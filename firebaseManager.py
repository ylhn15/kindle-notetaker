import pyrebase
import re
import os
import json


def get_firebase_config():
    exists = os.path.isfile('firebaseConfig.json')
    if exists:
        with open('firebaseConfig.json') as config:
            return json.load(config)


config = get_firebase_config()
firebase = pyrebase.initialize_app(config)
DATABASE = firebase.database()


def write_quote_to_db(data):
    extracted_quote = re.findall(r'"([^"]*)"', data)
    if len(extracted_quote) > 0:
        data_dict = {"quote": extracted_quote[0], "source": extracted_quote[1]}
        DATABASE.child("quotes").push(data_dict)
