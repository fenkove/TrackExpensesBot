import db_helper
import datetime
from config import *


def total_spent_per(period):
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year

    if period == "this month":
        period = "month"
        value = month
    elif period == "last month":
        period = "month"
        value = month-1
    elif period == "this year":
        period = "year"
        value = year
    elif period == "last year":
        period = "year"
        value = year-1
    else:
        print("Invalid period value")
    amount = get_total_spent_by_period(period, value)
    return amount


def get_total_spent_by_period(period, value):
    connection = db_helper.prepare_sqlite_connection()
    cursor = connection.cursor()
    sql = f"SELECT amount FROM {EXPENSES_TABLE} WHERE {period} = {value}"
    amount = 0
    for row in cursor.execute(sql):
        amount += row[0]
    return amount
