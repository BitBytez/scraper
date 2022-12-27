from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GSheetWriter:
    def __init__(self) -> None:
        creds = None
        SCOPES = ["https://www.googleapis.com/auth/drive",
                  "https://www.googleapis.com/auth/drive.file",
                  "https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/gmail.send"]
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        self.sheetService = build('sheets', 'v4', credentials=creds)

    def createSheet(self, title):
        sheet = self.sheetService.spreadsheets().create(body={
            'properties': {
                'title': title
            }
        }, fields='spreadsheetId').execute()
        return sheet.get('spreadsheetId')

    def insertIntoSheet(self, sheetID, values):
        self.sheetService.spreadsheets().values().update(
            spreadsheetId=sheetID,
            valueInputOption="USER_ENTERED",
            body={'values': values}, range="A1").execute()
