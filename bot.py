# - *- coding: utf- 8 - *-

import sqlite3
import telebot
import config
import db_helper
import markups as m
import reports as r
from config import *

app = telebot.TeleBot(config.TOKEN)
amount = 0
category = ""
description = ""
datetime = ""
categories = []


@app.message_handler(commands=['start'])
def start_message(message):
    app.send_message(message.chat.id, "Select action", reply_markup=m.keyboard_start)


@app.message_handler(commands=['help'])
def show_help(message):
    info = get_categories_info_sql()
    app.send_message(message.chat.id, info, reply_markup=m.keyboard_start)


def get_categories_info_sql():
    categories_info = ""
    cursor = db_helper.prepare_categories_table()
    sql = f"SELECT category, description FROM {CATEGORIES_TABLE}"
    for row in cursor.execute(sql):
        categories_info = categories_info + row[0] + ": " + row[1] + "\n"
    return categories_info

@app.message_handler(commands=['submit'])
def submit_expense(message):
    app.send_message(message.chat.id, 'Enter amount')
    app.register_next_step_handler(message, get_amount)


def get_amount(message):
    global amount
    try:
        amount = int(message.text)
        app.send_message(message.chat.id, 'Add comment')
        app.register_next_step_handler(message, get_comment)
    except ValueError:
        app.send_message(message.chat.id, 'Must be an integer value')
        start_message(message)


def get_comment(message):
    global description
    description = str(message.text)
    categories_keyboard = m.generate_categories_keyboard()
    app.send_message(message.chat.id, 'Select category', reply_markup=categories_keyboard)
    app.register_next_step_handler(message, get_category)


def get_category(message):
    global category
    category = message.text
    app.send_message(message.chat.id, 'Check record', reply_markup=m.keyboard_save)
    record = prepare_record(amount, category, description)
    check_record(message, record)


def prepare_record(amount, category, description):
    import datetime

    now = datetime.datetime.now()
    record = (amount,
               category,
               description,
               now.strftime("%x"),
               now.strftime("%W"),
               now.strftime("%m"),
               now.strftime("%Y"))
    return record

def check_record(message, record):
    if config.DB_MAIN_TABLE == "test":
        app.send_message(message.chat.id, 'this is test record')
    app.send_message(message.chat.id, f'Amount: {str(record[0])} UAH\nCategory: {record[1]}\nComment: {record[2]}', reply_markup=m.keyboard_save)


@app.message_handler(commands=['save'])
def save_record(message):
    if amount == 0 or category == "":
        print("Cannot save empty values")
    else:
        connection = db_helper.prepare_sqlite_connection()
        cursor = connection.cursor()
        record = prepare_record(amount, category, description)

        try:
            cursor.execute(f"INSERT INTO {EXPENSES_TABLE} VALUES (?,?,?,?,?,?,?)", record)
            connection.commit()
            print("Record has been saved successfully with ID: " + str(cursor.lastrowid))
            app.send_message(message.chat.id, 'SAVED', reply_markup=m.keyboard_start)
        except sqlite3.OperationalError:
            print("Record not saved due to operational error")
            app.send_message(message.chat.id, 'NOT SAVED', reply_markup=m.keyboard_start)
        finally:
            connection.close()


def keep_private(message, my_id):
    if str(message.chat.id) != my_id:
        message.text = "alien"
        return message


@app.message_handler(commands=['cancel'])
def save_record(message):
    app.send_message(message.chat.id, 'NOT SAVED', reply_markup=m.keyboard_start)


@app.message_handler(content_types=['text'])
def send_text(message):
    keep_private(message, config.CHAT_ID)
    request = message.text.lower()
    if request == 'submit expense':
        submit_expense(message)
    elif request == 'report':
        app.send_message(message.chat.id, 'Choose a period', reply_markup=m.keyboard_report)
    elif request in ('this month', 'last month', 'this year', 'last year'):
        spent_amount = r.total_spent_per(request)
        app.send_message(message.chat.id, f"Total spent per {request}: {str(spent_amount)} UAH", reply_markup=m.keyboard_start)
    elif request == 'help':
        show_help(message)
    elif request == 'alien':
        app.send_message(message.chat.id, 'Sorry, this bot is for private use only', reply_markup=m.keyboard_start)
    else:
        app.send_message(message.chat.id, "I don't understand you", reply_markup=m.keyboard_start)


app.polling(none_stop=True)
