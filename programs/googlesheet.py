import gspread
from oauth2client.service_account import ServiceAccountCredentials
from images_functions import *
# use creds to create a client to interact with the Google Drive API
scope = []
creds = None
client = None
sheet1 = None
sheet2 = None

try:
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('../../client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet1 = client.open("MK data").sheet1
    sheet2 = client.open("MK data").get_worksheet(1)
except:
    pass


def update(values, page, column, line):
    try:
        sheet = client.open("MK data").get_worksheet(page)
        # Select a range
        cell_list = sheet.range(column + str(line) + ':'+ column + str(line - 1 + len(values)))
        for i, cell in enumerate(cell_list):
            cell.value = values[i]
        # Update in batch
        sheet.update_cells(cell_list)
        print("UPDATED GoogleSheet page " + str(page+1))
    except:
        print(sys.exc_info()[0])


def update4Column(values, page, column, line):
    sheet = client.open("MK data").get_worksheet(page)
    print("yolo1")
    # Select a range
    nb_player = len(values)
    print("yolo2")
    cell_list = sheet.range(column + str(line) + ':'+ chr(ord(column)+nb_player-1) + str(line - 1 + len(values[0])))
    for i, cell in enumerate(cell_list):
        cell.value = values[int(i%nb_player)][int(i/nb_player)]
    # Update in batch
    sheet.update_cells(cell_list)
    print("UPDATED GoogleSheet page " + str(page+1))


def insert(values, index):
    sheet.col_values(values, index)


def set_positions_on_googlesheet(array):
    nb_player = len(array)
    final_array = []
    for player in range(nb_player):
        total_frame = len(array[player])
        array_purcent_time = []
        for position in range(1,13):
            array_purcent_time.append(array[player].count(position)/total_frame*100)
        final_array.append(array_purcent_time)
    update4Column(final_array, 1, chr(ord('B')), 2)


def set_places_on_googlesheet(liste_place, page):
    client.open("MK data").get_worksheet(page).clear()
    update4Column(liste_place, page, chr(ord('B')), 2)
