import gspread
from oauth2client.service_account import ServiceAccountCredentials
from images_functions import *

# use creds to create a client to interact with the Google Drive API
scope = []
creds = None
client = None
sheet = None
try:
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('../../client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("MK data").sheet1
except:
    pass


def update(values):
    # Select a range
    cell_list = sheet.range('B1:B'+str(len(values)))
    for i, cell in enumerate(cell_list):
        cell.value = values[i]
    # Update in batch
    sheet.update_cells(cell_list)


def insert(values, index):
    sheet.col_values(values, index)
