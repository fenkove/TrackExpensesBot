import pymongo
import config

def prepare_main_collection():
    client = pymongo.MongoClient(config.MONGO_DB_URL)
    mydb = client[config.DB_NAME]
    return mydb[config.DB_MAIN_TABLE]

def prepare_categories_collection():
    client = pymongo.MongoClient(config.MONGO_DB_URL)
    mydb = client[config.DB_NAME]
    return mydb[config.DB_CATEGORIES_TABLE]
