from pymongo import MongoClient, IndexModel, ASCENDING
from conf import MONGO_URL
from utils import check_ip

def get_settings():
    conn = MongoClient(MONGO_URL)
    settings = conn.main.static.find_one({"id":"settings"})
    conn.close()
    return settings


def create_indexes():
    conn = MongoClient(MONGO_URL)
    conn.main.static.create_indexes([
        IndexModel([("id",ASCENDING)],unique=True)
    ])
    conn.main.teams.create_indexes([
        IndexModel([("ip",ASCENDING)],unique=True)
    ])
    conn.close()

def create_settings():
    conn = MongoClient(MONGO_URL)
    conn.main.static.update_one({"id":"settings"},{"$setOnInsert":{"id":"settings","mode":"init"}},upsert=True)
    conn.close()

def updateInitState(i):
    conn = MongoClient(MONGO_URL)
    conn.main.static.update_one({"id":"settings"},{"$set":{"state":i}})
    conn.close()

def getInitState():
    conn = MongoClient(MONGO_URL)
    data = conn.main.static.find_one({"id":"settings"})
    conn.close()
    if "state" in data:
        return data["state"]
    else:
        return 0

def init_teams(teams:dict):
    req = []

    for k in teams.keys():
        if check_ip(teams[k]):
            req.append({"name":k,"ip":teams[k]})
        else:
            return False

    if len(req) > 0:
        conn = MongoClient(MONGO_URL)
        conn.main.teams.delete_many({})
        conn.main.teams.insert_many(req)
        conn.close()
        return True
    return False
