from telebot import types
import db_helper


keyboard_report = types.ReplyKeyboardMarkup(True,True)
keyboard_report.row('Last month', 'This month')
keyboard_report.row('Last year', 'This year')

keyboard_start = types.ReplyKeyboardMarkup(True,True)
keyboard_start.row('Help', 'Report', 'Submit Expense')

keyboard_save = types.ReplyKeyboardMarkup(True,True)
keyboard_save.row('/cancel', '/save')


categories = []
def load_categories():
    mycol = db_helper.prepare_categories_collection()
    mydoc = mycol.find()
    for x in mydoc:
        categories.append(x['category'])
    return tuple(categories)


def load_categories_sqlite():
    categories = []
    cursor = db_helper.prepare_categories_table()
    sql = "SELECT category FROM categories"
    for row in cursor.execute(sql):
        categories.append(row[0])
    return tuple(categories)


cats = load_categories_sqlite()


def generate_categories_keyboard():
    keyboard_categories = types.ReplyKeyboardMarkup(True,True)
    x = 0
    y = 3
    for z in range(len(cats)//3):
        keyboard_categories.row(*cats[x:y])
        x = y
        y += 4
    return keyboard_categories
