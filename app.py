from flask import Flask, render_template, url_for, redirect
import re
import random
import html
import os
import time


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload



app = Flask(__name__)





#      _       _        _
#   __| | __ _| |_ __ _| |__   __ _ ___  ___
#  / _` |/ _` | __/ _` | '_ \ / _` / __|/ _ \
# | (_| | (_| | || (_| | |_) | (_| \__ \  __/
#  \__,_|\__,_|\__\__,_|_.__/ \__,_|___/\___|
#



# Connect to Google Sheets
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
     "https://www.googleapis.com/auth/drive"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)
service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)



DATABASE_NAME = "quadegories"


def initialize():
    db = client.create(DATABASE_NAME)
    db.share('peter.e.francis.databases@gmail.com', perm_type='user', role='writer')
    return None


local_data = {}

def check_local_data_up_to_date(name):
    return name in local_data and time.time() - local_data[name]['time'] <= 60

def get_local_data(name):
    return local_data[name]['data']

def set_local_data(name, data):
    local_data[name] = {
        'data': data,
        'time': time.time()
    }
    return None





def get_sheet(sheet_name):
    if not check_local_data_up_to_date('sheet-' + sheet_name):
        set_local_data('sheet-' + sheet_name, client.open(DATABASE_NAME).worksheet(sheet_name))
    return get_local_data('sheet-' + sheet_name)

def get_sheet_keys(sheet_name):
    return get_sheet(sheet_name).row_values(1)

def row_dict_to_arr(sheet_name, row_dict):
    return [row_dict[key] if key in row_dict else "" for key in get_sheet_keys(sheet_name)]

def update_row(sheet_name, row_dict):
    '''
        looks for row with id == row_dict['id']
        if row_dict['id'] is None or no matching id is found, then adds a row
        otherwise, update
    '''

    sheet = get_sheet(sheet_name)

    loc = sheet.find(str(row_dict['id']))
    if loc is None or loc.col != get_sheet_keys(sheet_name).index('id') + 1:
        sheet.append_row(row_dict_to_arr(sheet_name, row_dict))
    else:
        for col, key in enumerate(get_sheet_keys(sheet_name)):
            if key in row_dict:
                sheet.update_cell(loc.row, col + 1, row_dict[key])

    return None

def get_next_id(sheet_name):
    sheet = get_sheet(sheet_name)
    return int(sheet.cell(sheet.row_count, 1).value) + 1





COLLECTIONS = {
    'beginner': {'name': 'Beginner', 'description': 'Simple Quadegories for younger players or beginners'},
    'expert': {'name': 'Expert', 'description': 'Challenging Quadegories from an eclectic variety of sources'},
    'harrypotter': {'name': 'Harry Potter', 'description': 'Magical quadegories from the famous seven-book series'},
}





def get_collection(collection_name):
    return get_sheet(collection_name).get_all_records()


def get_quad(collection_name, game_id):
    for quad in get_sheet(collection_name).get_all_records():
        if quad['id'] == game_id:
            return quad
    return None






#                  _             _
#   ___ ___  _ __ | |_ ___ _ __ | |_
#  / __/ _ \| '_ \| __/ _ | '_ \| __|
# | (_| (_) | | | | ||  __| | | | |_
#  \___\___/|_| |_|\__\___|_| |_|\__|




ERROR_MSG = {
    401: "You must be logged in to view this page.",
    403: "You don't have access to this page.",
    404: "The page you're looking for doesn't exist.",
    429: "Slow down... too many attempts.",
    500: "Server error.",
    ':(': "Hmmm.... not really sure what went wrong. If tihs problem persists, contact <a href='htttp://PeterEFrancis.com'>Peter E. Francis</a>."
}


@app.route('/error/<int:num>')
def error_page(num, e=None):
    msg = ""
    if num in ERROR_MSG:
        msg = ERROR_MSG[num]
    else:
        msg = ERROR_MSG[':(']
    return render_template(
        'error.html',
        footer = get_footer(),
        num = num,
        msg = msg,
        e = e
    ), num



@app.errorhandler(401)
def err401(e):
    return error_page(401), 401

@app.errorhandler(403)
def err403(e):
    return error_page(403), 403

@app.errorhandler(404)
def err404(e):
    return error_page(404), 404

@app.errorhandler(429)
def err429(e):
    return error_page(429), 429

@app.errorhandler(500)
def err500(e):
    return error_page(500), 500




def get_footer():
    return render_template('footer.html')

def get_header(collection=None, quad_id=None):
    return render_template(
        'header.html',
        COLLECTIONS = COLLECTIONS,
        collection=collection,
        quad_id=quad_id
    )



@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        footer = get_footer()
    )



@app.route('/game')
def choose_collection():
    return render_template(
        'choose-collection.html',
        collections=COLLECTIONS,
        header=get_header(),
        footer=get_footer()
    )



@app.route('/game/<string:collection>')
def collectionInfo(collection):
    if collection not in COLLECTIONS:
        return error_page(404)
    return render_template(
        'collection-info.html',
        collection=collection,
        COLLECTIONS=COLLECTIONS,
        collection_data=get_collection(collection),
        header=get_header(collection=collection),
        footer=get_footer()
    )


@app.route('/game/<string:collection>/<int:choice>')
def game(collection, choice):
    quad = get_quad(collection, choice)
    if quad is None:
        return error_page(404)

    return render_template(
        'game.html', 
        collection=collection,
        collection_name=COLLECTIONS[collection]['name'],
        quad=quad,
        header=get_header(collection=collection, quad_id=choice),
        footer=get_footer(),
        next=f'/game/{collection}/{choice + 1}' if choice + 1 < len(get_collection(collection)) else f'/game/{collection}'
    )







if __name__ == "__main__":
    app.debug = True
    app.run(port=2005)
