from __future__ import print_function
import pickle
import string
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pyasn1_modules.rfc2459 import ValidationParms

# make a function that can be triggered somehow
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '<id here>'
TEMP_SHEET = '<id here>'
RANGE_NAME = 'Map Comps!A1:Z52'
RANGE_NAME2 = 'Map Stats!A1:G30'
creds = None
service = None

def coltoLetter(n):
    name = ''
    while n > 0:
        n, r = divmod (n - 1, 26)
        name = chr(r + ord('A')) + name
    return name

def initialize():
    global creds
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
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
    global service
    service = build('sheets', 'v4', credentials=creds)

def getSheet():
    global service
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME, majorDimension='COLUMNS').execute()
    values = result.get('values', [])
    return values

def getTempSheet():
    global service
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=TEMP_SHEET,
                                range=RANGE_NAME2, majorDimension='COLUMNS').execute()
    values = result.get('values', [])
    return values

def updateStat(map_string, column):
    sheet = getTempSheet()
    for letter in range(len(sheet)):
        for index in range(len(sheet[letter])):
            if sheet[letter][index].lower().startswith(map_string):
                old_value = int(sheet[letter+column][index])
                request = service.spreadsheets().values().update(spreadsheetId=TEMP_SHEET, range=('Map Stats!'+coltoLetter(letter+column+1)+str(index+1)), valueInputOption='USER_ENTERED', body={'values': [[str(old_value+1)]]})
                response = request.execute()

def return_hero_comp(map_string):
    sheet = getSheet()
    for letter in range(len(sheet)):
        for index in range(len(sheet[letter])):
            if sheet[letter][index].lower().startswith(map_string):
                result_string = '```\n' + sheet[letter][index].upper() + '\n' + '\n'.join([sheet[letter2][index+1] + ' ' + ', '.join(sheet[letter2][index+2:index+8]) for letter2 in range(letter+1, letter+4)]) + '\n' + sheet[letter][index+1] + '\n```'
                return result_string
    return 'No result!'

initialize()
updateStat('lij', 2)
