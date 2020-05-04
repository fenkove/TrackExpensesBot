import telebot
import config
import markups as m
import pymongo

app = telebot.TeleBot(config.TOKEN)
amount = 0
category = ""
desription = ""
datetime = ""

@app.message_handler(commands=['start'])
def start_message(message):
    app.send_message(message.chat.id, "Select action", reply_markup=m.keyboard_start)

@app.message_handler(commands=['submit'])
def submit_expense(message):
    app.send_message(message.chat.id, 'Enter amount')
    app.register_next_step_handler(message, get_amount)

def get_amount(message):
    global amount
    amount = int(message.text)
    app.send_message(message.chat.id, 'Select category', reply_markup=m.keyboard_categories)
    app.register_next_step_handler(message, get_category)

def get_category(message):
    global category
    category = message.text
    app.send_message(message.chat.id, 'Check record', reply_markup=m.keyboard_save)
    record = prepare_record(amount,category,desription)
    check_record(message, record)

def prepare_record(amount, category, description):
    import datetime

    now = datetime.datetime.now()
    week = now.strftime("%W")
    year = now.strftime("%Y")
    month = now.strftime("%m")
    datetime = now.strftime("%x")

    record = {"amount": amount, "category": category, "description": description, "date": datetime, "week": week, "month": month, "year": year}
    return record

def check_record(message, record):
    app.send_message(message.chat.id, f'Amount: {str(record["amount"])} UAH\nCategory: {record["category"]}', reply_markup=m.keyboard_save)

@app.message_handler(commands=['save'])
def save_record(message):
    client = prepare_db_client()
    mydb = client[config.DB_NAME]
    mycol = mydb[config.DB_TABLE]
    record = prepare_record(amount,category,desription)
    x = mycol.insert_one(record)
    if x:
        print("Record has been saved successfully with ID: "+str(x.inserted_id))

    app.send_message(message.chat.id, 'SAVED', reply_markup=m.keyboard_start)

def prepare_db_client():
    return pymongo.MongoClient(config.MONGO_DB_URL)

def get_report(period):
    client = prepare_db_client()
    mydb = client[config.DB_NAME]
    mycol = mydb[config.DB_TABLE]
    myquery = {"Description": "Novus"}
    mydoc = mycol.find(myquery)
    for x in mydoc:
        print(x)

@app.message_handler(commands=['cancel'])
def save_record(message):
    app.send_message(message.chat.id, 'NOT SAVED', reply_markup=m.keyboard_start)

@app.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'submit expense':
        submit_expense(message)
    elif message.text.lower() == 'report':
        app.send_message(message.chat.id, 'Reports are not ready yet', reply_markup=m.keyboard_start)
    elif message.text.lower() == 'settings':
        app.send_message(message.chat.id, 'Settings are not ready yet', reply_markup=m.keyboard_start)
    else:
        app.send_message(message.chat.id, 'Ти чьо ахуєл пьос?', reply_markup=m.keyboard_start)


app.polling(none_stop=True)