import base64
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def get_creds(SCOPES):
    creds = None

    # The file token.pickle is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
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
        "photoBytes": base64.base64encode
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