import telebot
import config
import db_helper
import markups as m
import reports as r

app = telebot.TeleBot(config.TOKEN)
amount = 0
category = ""
desription = ""
datetime = ""
categories = []

@app.message_handler(commands=['start'])
def start_message(message):
    # load_categories()
    app.send_message(message.chat.id, "Select action", reply_markup=m.keyboard_start)

@app.message_handler(commands=['help'])
def show_help(message):
    info = get_categories_info()
    app.send_message(message.chat.id, info, reply_markup=m.keyboard_start)


def get_categories_info():
    categories_info = ""
    mycol = db_helper.prepare_categories_collection()
    mydoc = mycol.find()
    for x in mydoc:
        categories_info = categories_info + x['category'] + ": " + x['description'] + "\n";
    return categories_info

@app.message_handler(commands=['submit'])
def submit_expense(message):
    app.send_message(message.chat.id, 'Enter amount')
    app.register_next_step_handler(message, get_amount)

def get_amount(message):
    global amount
    amount = int(message.text)
    app.send_message(message.chat.id, 'Add comment')
    app.register_next_step_handler(message, get_comment)

def get_comment(message):
    global desription
    desription = str(message.text)
    categories_keyboard = m.generate_categories_keyboard()
    app.send_message(message.chat.id, 'Select category', reply_markup=categories_keyboard)
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
    if config.DB_MAIN_TABLE == "test":
        app.send_message(message.chat.id, 'this is test record')
    app.send_message(message.chat.id, f'Amount: {str(record["amount"])} UAH\nCategory: {record["category"]}\nComment: {record["description"]}', reply_markup=m.keyboard_save)


@app.message_handler(commands=['save'])
def save_record(message):
    if (amount == 0 or category == ""):
        print("Cannot save empty values")
    else:
        mycol = db_helper.prepare_main_collection()
        record = prepare_record(amount,category,desription)
        x = mycol.insert_one(record)
        if x:
            print("Record has been saved successfully with ID: "+str(x.inserted_id))
            app.send_message(message.chat.id, 'SAVED', reply_markup=m.keyboard_start)

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
