from flask import Blueprint, redirect, request, jsonify, make_response
import conf, utils
from utils import db
app = Blueprint('init', __name__)

@app.route("/next", methods=["GET","POST"])
def next_state():
    if conf.APP_STATUS == "init":
        state = db.getInitState()
        if state == 0:
            return create_json_response(None,state)
        if state == 1:
            return create_json_response(init1(request.get_json()),state)
        if state == 2:
            return create_json_response(init2(request.get_json()),state)
        if state == 3:
            return create_json_response(init3(request.get_json()),state)
        
    return redirect("/")

@app.route("/back")
def prev_state():
    if conf.APP_STATUS == "init":
        state = db.getInitState()
        if state <= 0:
            return redirect("/init/0")
        else:
            db.updateInitState(state-1)
            return redirect(f"/init/{state-1}")
    else:
        return redirect("/")

def create_json_response(data,state):
    if data is None:
        data = {"status":True}

    if "status" not in data:
        data["status"] = True

    if data["status"] == True:
        goto = state+1
        if "goto" in data:
            goto = data["goto"]
            del data["goto"]
        data["redirect"] = f"/init/{goto}"
        db.updateInitState(goto)
    
    return make_response(jsonify(data), 200)

def init1(data):
    if data["config_method"] == "create":
        return None
    elif data["config_method"] == "upload":
        return {"status":False,"msg":"Not implemented yet!"}

def init2(data):
    if not db.init_teams(data):
        return {"status":False,"msg":"Ip configuration refused (Send valid IP address and at least 1 IP)"}

def init3(data):
    required_keys = ("code","regex","duplicated","temporised_submit","multiple_submit","flag_expiring")
    if not all([ ele in data.keys() for ele in required_keys ]):
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