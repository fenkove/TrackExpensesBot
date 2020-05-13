from telebot import types
import config
import telebot
import pymongo
import db_helper



keyboard_start = types.ReplyKeyboardMarkup(True,True)
keyboard_start.row('Help', 'Report', 'Submit Expense')

keyboard_save = types.ReplyKeyboardMarkup(True,True)
keyboard_save.row('/cancel', '/save')



categories = []
def load_categories():
    client = db_helper.prepare_db_client()
    mydb = client[config.DB_NAME]
    mycol = mydb[config.DB_CATEGORIES_TABLE]
    mydoc = mycol.find()
    for x in mydoc:
        categories.append(x['category'])
    return tuple(categories)

cats = load_categories()

def generate_categories_keyboard():
    keyboard_categories = types.ReplyKeyboardMarkup(True,True)
    x = 0
    y = 3
    for z in range(len(cats)//3):
        keyboard_categories.row(*cats[x:y])
        x = y
        y += 4
    return keyboard_categories
