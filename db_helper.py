import pymongo
import config

def prepare_db_client():
    return pymongo.MongoClient(config.MONGO_DB_URL)