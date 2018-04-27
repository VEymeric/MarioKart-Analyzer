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
except:
    pass


def update(values, page, column, line):
    """ màj une colonne sur un googlesheet"""
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
        print("No connection : ", sys.exc_info()[0])


def update_4_column(values, page, column, line):
    """ on évite de faire 4 requête si on doit la même chose pour les 4 joueurs"""
    try:
        sheet = client.open("MK data").get_worksheet(page)
        # Select a range
        nb_player = len(values)
        cell_list = sheet.range(column + str(line) + ':'+ chr(ord(column)+nb_player-1) + str(line - 1 + len(values[0])))
        for i, cell in enumerate(cell_list):
            cell.value = values[int(i%nb_player)][int(i/nb_player)]
        # Update in batch
        sheet.update_cells(cell_list)
        print("UPDATED GoogleSheet page " + str(page+1))
    except:
        print("No connection : ", sys.exc_info()[0])


def set_positions_on_googlesheet(array):
    nb_player = len(array)
    final_array = []
    for player in range(nb_player):
        total_frame = len(array[player])
        array_purcent_time = []
        for position in range(1,13):
            array_purcent_time.append(array[player].count(position)/total_frame*100)
        final_array.append(array_purcent_time)
    update_4_column(final_array, 1, chr(ord('B')), 2)


def set_places_on_googlesheet(liste_place, page):
    try:
        client.open("MK data").get_worksheet(page).clear()
    except:
        print("No connection")
        return
    update_4_column(liste_place[0], page, chr(ord('B')), 2)
    update(liste_place[1], page, 'A', 2)

