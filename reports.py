import db_helper
import datetime


def total_spent_per(period):
    mycoll = db_helper.prepare_main_collection()
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    myquery = {}

    if period == "this month":
        myquery = {"month": "0" + str(month)}
    elif period == "last month":
        myquery = {"month": "0" + str(month - 1)}
    elif period == "this year":
        myquery = {"year": str(year)}
    elif period == "last year":
        myquery = {"year": str(year - 1)}
    else:
        print("Invalid period value")
    amount = get_total_spent_by_period(mycoll, myquery)
    return amount


def get_total_spent_by_period(mycoll, myquery):
    amount = 0
    results = mycoll.find(myquery)
    for x in results:
        amount += int(x['amount'])
    return amount
