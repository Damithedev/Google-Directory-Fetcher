from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/directory.readonly']

Contacts_List = []

def main():
    """Shows basic usage of the Docs API. Prints the title of a sample document."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    emaillist=[]
    namelist = []
    givennamelist = []
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'cred.json',
                SCOPES,
                redirect_uri='http://localhost:8080/',
                  # Add this line to request offline access.
            )

            creds = flow.run_local_server(
                access_type='offline',
                host='localhost',
                authorization_prompt_message='Please visit this URL: {url}',
                success_message='The auth flow is complete; you may close this window.',
            )
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('people', 'v1', credentials=creds)

        # Initialize variables for pagination
        page_token = None
        count = 0

        while True:
            # Retrieve the document's contents from the Docs service.

            results = service.people().listDirectoryPeople(
                readMask="emailAddresses,names",
                sources=['DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE'],
                pageToken=page_token
            ).execute()


            connections = results.get('people', [])

            for person in connections:
                emails = person.get('emailAddresses', [])
                names = person.get('names', [])

                if names:
                    name = names[0].get('displayName')
                    givenname = names[0].get('givenName')
                    givennamelist.append(givenname)
                    namelist.append(name)
                else:
                    name = 'Student'
                    givenname = 'Student'
                    namelist.append(name)
                    givennamelist.append(givenname)
                if emails:
                    email = emails[0].get('value')

                    emaillist.append(email)
                    count += 1
                else:
                    email = ''
                    email.append(name)

            page_token = results.get('nextPageToken')
            if not page_token:
                break


    except HttpError as err:
        print(err)
    dict = {'name': namelist, 'email List': emaillist, 'Given name': givennamelist}
    info = pd.DataFrame(dict)
    print(info)
    info.to_csv('info.csv')
if __name__ == '__main__':
    main()
