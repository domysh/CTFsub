from flask import Blueprint, request
import conf
from utils.db import get_engine_response

app = Blueprint('engine', __name__)

@app.route("/request", methods=["POST"])
def send_engine_request():
    from utils.engine import send_request
    data = request.get_json()
    id_req = send_request(data)
    if conf.DEBUG: print("Sended request:", data,flush=True)
    return {"id":id_req}

@app.route("/response/<req_id>")
def get_engine_response_api(req_id):
    resp = get_engine_response(req_id)
    if resp is None:
        return {"status":False,"error":"No data found"}
    del resp["_id"]
    return {"status":True,"data":resp}