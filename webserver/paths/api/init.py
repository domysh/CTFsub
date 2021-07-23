from flask import Blueprint, redirect, request, jsonify, make_response
import conf, utils
from utils import db
app = Blueprint('init', __name__)


def load_init_state(go_next):
    state = db.getInitState()
    if state == 0:
        return create_json_response(None,state,go_next)
    if state == 1:
        return create_json_response(init1(request.get_json()),state,go_next)
    if state == 2:
        return create_json_response(init2(request.get_json()),state,go_next)
    if state == 3:
        return create_json_response(init3(request.get_json()),state,go_next)
    if state == 4:
        return create_json_response(init4(request.get_json()),state,go_next)

@app.route("/save", methods=["GET","POST"])
def save_state():
    if conf.APP_STATUS == "init":
        res = load_init_state(None)
        if not res is None:
            return res
    return redirect("/")

@app.route("/next", methods=["GET","POST"])
def next_state():
    if conf.APP_STATUS == "init":
        res = load_init_state(True)
        if not res is None:
            return res
    return redirect("/")

@app.route("/back")
def prev_state_forced():
    if conf.APP_STATUS == "init":
        state = db.getInitState()
        if state <= 0:
            return redirect("/init/0")
        else:
            db.updateInitState(state-1)
            return redirect(f"/init/{state-1}")
    else:
        return redirect("/")

@app.route("/state/<init_id>")
def get_actual_state(init_id):
    if conf.APP_STATUS == "init":
        data = None
        if init_id == "2":
            data = db.get_teams()
            if len(data) == 0:
                data = None
        elif init_id == "3":
            data = db.get_flag_submit_config()
        elif init_id == "4":
            data = db.get_attack_config()
        
        if data is None:
            return make_response(jsonify({"status":False,"msg":"No state found!"}), 200)
        else:
            return make_response(jsonify({"status":True,"data":data}), 200)
    else:
        return redirect("/")



def create_json_response(data,state,go_next):
    if data is None:
        data = {"status":True}

    if "status" not in data:
        data["status"] = True

    if data["status"] == True and not go_next is None:
        if go_next:
            goto = state+1
            if "goto" in data:
                goto = data["goto"]
                del data["goto"]
        else:
            goto = state-1 if state > 0 else 0
        
        data["redirect"] = f"/init/{goto}"
        db.updateInitState(goto)
    
    return make_response(jsonify(data), 200)

def init1(data):
    if data["config_method"] == "create":
        return None
    elif data["config_method"] == "upload":
        try:
            res = init2(data["data"]["init"]["2"])
            if not res is None and not res["status"]:
                return {"status":False,"msg":"Invalid file uploaded!"}
            res = init3(data["data"]["init"]["3"])
            if not res is None and not res["status"]:
                return {"status":False,"msg":"Invalid file uploaded!"}
            res = init4(data["data"]["init"]["4"])
            if not res is None and not res["status"]:
                return {"status":False,"msg":"Invalid file uploaded!"}
            if len(data["data"]["pip_install"]) > 0:
                from utils.engine import send_request
                from utils.db import get_engine_response
                import time
                id_req = send_request({
                    "type":"pip_install",
                    "libs":" ".join(data["data"]["pip_install"])
                })
                for _ in range(150):
                    res = get_engine_response(id_req)
                    if res is None:
                        time.sleep(1)
                    else:
                        if res["data"][0]:
                            return {"goto":5}
                        else:
                            return {"status":True,"msg":"Python libraries install failed! (pip raised an error!). The configs has been loaded, you can continue to use CTFsub!", "goto":5}
                return {"status":True,"msg":"Python libraries install failed! (Timeout error on the response by CTFsub engine). The configs has been loaded, you can continue to use CTFsub!", "goto":5}
            return {"goto":5}
        except KeyError:
            import traceback
            traceback.print_exc()
            return {"status":False,"msg":"Invalid file uploaded!"}

def init2(data):
    if not db.init_teams(data):
        return {"status":False,"msg":"Ip configuration refused (Send valid IP address and at least 1 IP)"}

def init3(data):
    required_keys = ("code","regex","duplicated","temporised_submit","multiple_submit","flag_expiring")
    if not all( ele in data.keys() for ele in required_keys ):
        return {"status":False,"msg":"Invalid json request! Not all paramethers were sended"}
    
    if type(data["code"]) == str:
        errors = utils.get_syntax_errors(data["code"])
        if errors:
            return {"status":False,"msg":"The submit code have syntax errors:\n\n"+errors}
    else:
        return {"status":False,"msg":"Invalid code sended!"}
    
    db.set_flag_submit_code(data["code"])

    if not data["regex"] is None:
        if type(data["regex"]) == str:
            if not utils.check_valid_regex(data["regex"]):
                return {"status":False,"msg":"Invalid regex sended!"}
        else:
            return {"status":False,"msg":"Invalid regex sended!"}

    db.set_flag_regex(data["regex"])

    if type(data["duplicated"]) != bool:
        return {"status":False,"msg":"Invalid data sended for duplicated!"}
    
    db.set_flag_duplicated(data["duplicated"])

    if not data["temporised_submit"] is None:
        if type(data["temporised_submit"]) == dict:
            temporised_submit = data["temporised_submit"]
            if "range" not in temporised_submit or type(temporised_submit["range"]) not in (int, float) or temporised_submit["range"] <= 0:
                return {"status":False,"msg":"Invalid data sended for temporised_submit (range is not valid)!"}
            if "attacks" not in temporised_submit or type(temporised_submit["attacks"]) != int or temporised_submit["attacks"] <= 0:
                return {"status":False,"msg":"Invalid data sended for temporised_submit (attacks is not valid)!"}
            db.set_temporised_submit({"range":temporised_submit["range"],"attacks":temporised_submit["attacks"]})
        else:
            return {"status":False,"msg":"Invalid data sended for temporised_submit!"}
    else:
        db.set_temporised_submit(None)
    
    if not data["multiple_submit"] is None:
        if type(data["multiple_submit"]) != int or data["multiple_submit"] <= 0:
            return {"status":False,"msg":"Invalid data sended for multiple_submit!"}
    
    db.set_multiple_submit(data["multiple_submit"])

    if not data["flag_expiring"] is None:
        if type(data["flag_expiring"]) != int or data["flag_expiring"] <= 0:
            return {"status":False,"msg":"Invalid data sended for flag_expiring!"}
    
    db.set_flag_expiring(data["flag_expiring"])

def init4(data):

    required_keys = ("attack_tick_time","attack_timeout","attack_workers","autoblacklist")
    if not all( ele in data.keys() for ele in required_keys ):
        return {"status":False,"msg":"Invalid json request! Not all paramethers were sended"}

    if not data["attack_tick_time"] is None:
        if type(data["attack_tick_time"]) != int or data["attack_tick_time"] <= 0:
            return {"status":False,"msg":"Invalid data sended for Tick time"}
    
    db.set_attack_tick_time(data["attack_tick_time"])

    if not data["attack_timeout"] is None:
        if type(data["attack_timeout"]) != int or data["attack_timeout"] <= 0:
            return {"status":False,"msg":"Invalid data sended for Timeout"}
    
    db.set_attack_timeout(data["attack_timeout"])

    if not data["attack_workers"] is None:
        if type(data["attack_workers"]) != int or data["attack_workers"] <= 0:
            return {"status":False,"msg":"Invalid data sended for Workers"}
    
    db.set_attack_workers(data["attack_workers"])

    if not data["autoblacklist"] is None:
        if type(data["autoblacklist"]) != dict:
            return {"status":False,"msg":"Invalid data sended for Auto Blacklist"}
    
        required_keys = ("max_fails","retry_loop_times")
        if not all( ele in data["autoblacklist"].keys() for ele in required_keys ):
            return {"status":False,"msg":"Invalid json request! Not all paramethers were sended in blacklist"}
        
        if not data["autoblacklist"]["max_fails"] is None:
            if type(data["autoblacklist"]["max_fails"]) != int or data["autoblacklist"]["max_fails"] <= 0:
                return {"status":False,"msg":"Invalid data sended for blacklist (Invalid Failure Times)"}
        else:
            return {"status":False,"msg":"Invalid data sended for blacklist (failure times is compulsory)"}
        
        if not data["autoblacklist"]["retry_loop_times"] is None:
            if type(data["autoblacklist"]["retry_loop_times"]) != int or data["autoblacklist"]["retry_loop_times"] <= 0:
                return {"status":False,"msg":"Invalid data sended for blacklist (Invalid retry after)"}
        
        db.set_autoblacklist({
            "max_fails":data["autoblacklist"]["max_fails"],
            "retry_loop_times":data["autoblacklist"]["retry_loop_times"]
        })
    else:
        db.set_autoblacklist(None)