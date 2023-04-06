from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import requests

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
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
                r'C:\Users\XPC\OneDrive\Desktop\Budget Familiar\StreamlitBudget\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        #if not labels:
        #    print('No labels found.')
        #    return
        #print('Labels:')
        #for label in labels:
        #    print(label['name'])
            
        response = requests.get('https://gmail.googleapis.com/gmail/v1/users/jchavesm2017@gmail.com/messages', headers={ 'Authorization': 'Bearer ya29.a0Ael9sCN2pfDGmqoOcKle3Wwdvi-5daeJ1QbiKqHIFJNOPEKi-GwsuHlce2I-vBc94OyjwVBO9dS2v26PJKMBJaNnvaAk0aLPsdljhci9O5d0rrBikLbuuYshjPedVIlmcNv26EIGkXrKVje0UvCUZyw-Um9HaCgYKAXASARESFQF4udJhtGgPuMye43fbW6sd9lsa5Q0163' })
        response_json = response.json()
        #print(response_json)

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()