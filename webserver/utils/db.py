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

def set_config(key, data):
    conn = MongoClient(MONGO_URL)
    conn.main.static.update_one({"id":"settings"},{"$set":{key:data}})
    conn.close()

def set_flag_submit_code(code):
    set_config("submit_code", code)

def set_flag_regex(regex):
    set_config("flag_regex", regex)

def set_flag_duplicated(duplicate):
    set_config("duplicated_flags_allowed", duplicate)

def set_temporised_submit(temporised_settings):
    set_config("temporised_submit", temporised_settings)

def set_multiple_submit(multiple_submit):
    set_config("multiple_submit", multiple_submit)

def set_flag_expiring(flag_expiring):
    set_config("flag_expiring", flag_expiring)

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


