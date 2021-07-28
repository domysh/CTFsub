from pymongo import MongoClient, IndexModel, ASCENDING
from pymongo.errors import OperationFailure
import conf, time

def init():
    try:
        conn = MongoClient(conf.MONGO_URL)
        conn.admin.command("replSetInitiate",{"_id":"rs0","members":[{ "_id": 0, "host": "127.0.0.1:27017" }]})
        time.sleep(.5) # DB auto set itself as primary
    except OperationFailure as e: #Operation already done (code == 23) 
        if e.code != 23: raise e 
    finally:
        conn.close()
    create_indexes()
    create_settings()

def get_settings():
    conn = MongoClient(conf.MONGO_URL)
    settings = conn.main.static.find_one({"id":"settings"})
    conn.close()
    return settings

def create_indexes():
    conn = MongoClient(conf.MONGO_URL)
    conn.main.static.create_indexes([
        IndexModel([("id",ASCENDING)],unique=True),
        IndexModel([("expire",ASCENDING)],expireAfterSeconds=600)
    ])
    conn.main.teams.create_indexes([
        IndexModel([("ip",ASCENDING)],unique=True)
    ])
    conn.close()

def register_libraries(libs):
    configs = get_settings()
    installed_libs = libs
    if "installed_libs" in configs:
        installed_libs += configs["installed_libs"]
    installed_libs = list(set(installed_libs))
    conn = MongoClient(conf.MONGO_URL)
    conn.main.static.update_one({"id":"settings"},{"$set":{"installed_libs":installed_libs}})
    conn.close()
    
def create_response(id_data,data):
    from datetime import datetime
    conn = MongoClient(conf.MONGO_URL)
    conn.main.static.insert_one({"id":"engine_"+id_data,"data":data,"expire":datetime.now()})
    conn.close()

def create_settings():
    conn = MongoClient(conf.MONGO_URL)
    conn.main.static.update_one({"id":"settings"},{"$setOnInsert":{"id":"settings","mode":"init"}},upsert=True)
    conn.close()