from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import pandas as pd
import email


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def google_api():

    """Read the unread emails of verybusywagoner@gmail.com.
    Needs the file 'credentials.json' in the same folder as this script to work.
    At first utilisation, you need to click on the link displayed and confirm the access. Once done, re-execute the code.
    A token.json file is then automatically generated in the folder and the code should work just fine.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])

        if not messages:
            print('No labels found.')
            return
        email_body = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
            msg_str = msg['raw'].encode('utf-8')
            msg_str = base64.urlsafe_b64decode(msg_str).decode('utf-8')
            msg = email.message_from_string(msg_str)
            # email_body.append(base64.urlsafe_b64decode(msg['payload']['parts'][0]['body']['data']).decode("utf-8"))
            if msg.is_multipart():
                body = msg.get_payload()[0].get_payload()
            else:
                body = msg.get_payload()
            email_body.append(body)

        return pd.Series(email_body)

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    google_api()
    # print(res)
