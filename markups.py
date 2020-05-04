from telebot import types


keyboard_start = types.ReplyKeyboardMarkup(True,True)
keyboard_start.row('Settings', 'Report', 'Submit Expense')

keyboard_save = types.ReplyKeyboardMarkup(True,True)
keyboard_save.row('/cancel', '/save')

keyboard_categories = types.ReplyKeyboardMarkup(True,True)
keyboard_categories.row('Grocery', 'Car', 'Restaurants')