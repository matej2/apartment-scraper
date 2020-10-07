import base64
import json
import os
import pickle

from apartment_scraper.settings import BASE_DIR

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def get_creds(SCOPES):
    creds = None
    cred_dir = os.path.join(BASE_DIR, 'credentials.json')
    pickle_dir = os.path.join(BASE_DIR, 'token.pickle')

    # The file token.pickle is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(pickle_dir):
        with open(pickle_dir, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            config = json.loads(os.environ['CRED'])
            flow = InstalledAppFlow.from_client_config(config, SCOPES)
            host = os.environ['REDIRECT_URL'] if os.environ['REDIRECT_URL'] is not None else 'localhost'
            #flow.redirect_uri = os.environ['REDIRECT_URL']
            creds = flow.run_local_server(host=host, port=8080)
        # Save the credentials for the next run
        with open(pickle_dir, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def add_contact(apartment):
    creds = get_creds(['https://www.googleapis.com/auth/contacts'])

    service = build('people', 'v1', credentials=creds)

    created_obj = service.people().createContact(body={
        "names": [
            {
                "givenName": apartment.title
            }
        ],
        "phoneNumbers": [
            {
                'value': apartment.contact
            }
        ],
        "biographies": [
            {
                "value": f"Rent: {apartment.rent}"
            }
        ],
        "urls": [
            {
                "value": apartment.url
            }
        ]
    }).execute()

    if created_obj != None:
        return True
    else:
        return False

def add_picture(obj, pic):
    creds = get_creds(['https://www.googleapis.com/auth/contacts'])

    service = build('people', 'v1', credentials=creds)
    service.people().updateContactPhoto(obj.resourceName, body= {
        "photoBytes": base64.base64encode(pic)
    })

def add_sheet_data(values):
    creds = get_creds('https://www.googleapis.com/auth/spreadsheets')
    service = build('sheets', 'v4', credentials=creds)

    spreadsheet_id = os.environ('spreadsheet_id')
    worksheet_name = 'logs'
    cell_range_insert = 'A1'

    value_range_body = {
        'majorDimension': 'COLUMNS',
        'values': values
    }

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        valueInputOption='USER_ENTERED',
        range=worksheet_name + cell_range_insert,
        body=value_range_body
    ).execute()