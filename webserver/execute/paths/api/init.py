from flask import Blueprint, redirect, request, jsonify, make_response
import conf
from utils.db import (getInitState, updateInitState,
                        init_teams, get_flag_submit_code)
app = Blueprint('init', __name__)

@app.route("/next", methods=["GET","POST"])
def next_state():
    if conf.APP_STATUS == "init":
        state = getInitState()
        if state == 0:
            return create_json_response(None,state)
        if state == 1:
            return create_json_response(init1(request.get_json()),state)
        if state == 2:
            return create_json_response(init2(request.get_json()),state)
        
    return redirect("/")

@app.route("/back")
def prev_state():
    if conf.APP_STATUS == "init":
        state = getInitState()
        if state <= 0:
            return redirect("/init/0")
        else:
            updateInitState(state-1)
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
        updateInitState(goto)
    
    return make_response(jsonify(data), 200)

def init1(data):
    if data["config_method"] == "create":
        return None
    elif data["config_method"] == "upload":
        return {"status":False,"msg":"Not implemented yet!"}

def init2(data):
    if not init_teams(data):
        return {"status":False,"msg":"Ip configuration refused (Send valid IP address and at least 1 IP)"}

