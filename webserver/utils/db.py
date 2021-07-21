from pymongo import MongoClient
from conf import MONGO_URL
from utils import check_ip

def get_settings():
    conn = MongoClient(MONGO_URL)
    settings = conn.main.static.find_one({"id":"settings"})
    conn.close()
    return settings

def updateInitState(i):
    conn = MongoClient(MONGO_URL)
    conn.main.static.update_one({"id":"settings"},{"$set":{"state":i}})
    conn.close()

def getInitState():
    data = get_settings()
    if "state" in data:
        return data["state"]
    else:
        return 0

def get_engine_response(id_req):
    conn = MongoClient(MONGO_URL)
    res = conn.main.static.find_one({"id":"engine_"+id_req})
    conn.close()
    return res

def get_flag_submit_code():
    data = get_settings()
    if "submit_code" in data:
        return data["submit_code"]
    else:
        return False

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


