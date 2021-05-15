# Quotetaker
E-Mail yourself your favourite quotes. Primarily written to automatically save quotes shared with the Kindle E-Mail sharing, this tool can also be used to save self-written quotes.

## Format
The format depends on the format of the automatically written e-mails from the Kindle.
You can send your own quotes or notes in the following format:
```
"This is the quote" - "and this is the source"
```

## Dependencies

### Pyrebase
Install [Pyrebase](https://github.com/thisbejim/Pyrebase) by running `pip3 install pyrebase`

## Configuration

### E-Mail Credentials

If you don't have a file called credentials.json, the application will prompt you to put in your IMAP Server, the username and the password. 
All of these are stored locally as a *plain text file*! Use at your own risk.

### Firebase

Create a file called firebaseConfig.json and add the following:
```json
{
    "apiKey": "your-firebase-api-key",
    "authDomain": "your-project-auth-domain",
    "databaseURL": "your-database-url",
    "projectId": "your-project-id",
    "storageBucket": "your-storage-bucket",
    "messagingSenderId": "your-messaging-sender-id",
    "appId": "your-app-id"
}
```
All of the information is stored locally as a *plain text file*! Use at your own risk.
