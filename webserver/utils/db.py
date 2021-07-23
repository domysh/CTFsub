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

def set_attack_tick_time(attack_tick_time):
    set_config("attack_tick_time", attack_tick_time)

def set_attack_timeout(attack_timeout):
    set_config("attack_timeout", attack_timeout)

def set_attack_workers(attack_workers):
    set_config("attack_workers", attack_workers)

def set_autoblacklist(autoblacklist):
    set_config("autoblacklist", autoblacklist)

def get_flag_submit_config():
    configs = get_settings()
    required_keys = ("submit_code", "flag_regex", "duplicated_flags_allowed", "temporised_submit", "flag_expiring", "multiple_submit")
    if all( ele in configs.keys() for ele in required_keys ):
        return {
            "code":configs["submit_code"],
            "regex":configs["flag_regex"],
            "duplicated":configs["duplicated_flags_allowed"],
            "multiple":configs["multiple_submit"],
            "temporised_flags":configs["temporised_submit"],
            "expire":configs["flag_expiring"]
        }
def get_attack_config():
    configs = get_settings()
    required_keys = ("attack_tick_time","attack_timeout","attack_workers","autoblacklist")
    if all( ele in configs.keys() for ele in required_keys ):
        return {
            "attack_tick_time":configs["attack_tick_time"],
            "attack_timeout":configs["attack_timeout"],
            "attack_workers":configs["attack_workers"],
            "autoblacklist":configs["autoblacklist"]
        }

def get_config_dict():
    configs = get_settings()
    inits = {
        "2":get_teams(),
        "3":{
            "code":configs["submit_code"],
            "regex":configs["flag_regex"],
            "duplicated":configs["duplicated_flags_allowed"],
            "temporised_submit":configs["temporised_submit"],
            "multiple_submit":configs["multiple_submit"],
            "flag_expiring":configs["flag_expiring"]
        },
        "4":{
            "attack_tick_time":configs["attack_tick_time"],
            "attack_timeout":configs["attack_timeout"],
            "attack_workers":configs["attack_workers"],
            "autoblacklist":configs["autoblacklist"]
        }
    }
    pip_install = configs["installed_libs"] if "installed_libs" in configs else []

    return {
        "init":inits,
        "pip_install":pip_install,
    }


def get_teams():
    conn = MongoClient(MONGO_URL)
    res = {}
    for tm in conn.main.teams.find({}):
        res[tm["name"]] = tm["ip"]
    conn.close()
    return res

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


