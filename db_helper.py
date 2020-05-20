import pymongo
import config
import sqlite3

def prepare_main_collection():
    client = pymongo.MongoClient(config.MONGO_DB_URL)
    mydb = client[config.DB_NAME]
    return mydb[config.DB_MAIN_TABLE]

def prepare_categories_collection():
    client = pymongo.MongoClient(config.MONGO_DB_URL)
    mydb = client[config.DB_NAME]
    return mydb[config.DB_CATEGORIES_TABLE]

#sqlite3
def prepare_sqlite_connection():
    return sqlite3.connect(config.SQLITE3_DB_NAME)


def prepare_categories_table():
    conn = sqlite3.connect(config.SQLITE3_DB_NAME)  # или :memory: чтобы сохранить в RAM
    return conn.cursor()
