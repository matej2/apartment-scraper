import base64
import os

from googleapiclient.discovery import build
from google.oauth2 import service_account

from apartment_scraper.settings import BASE_DIR


def get_creds(SCOPES):
    cred_dir = os.path.join(BASE_DIR, os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    credentials = service_account.Credentials.from_service_account_file(
        cred_dir,
        scopes=SCOPES
    )
    return credentials

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