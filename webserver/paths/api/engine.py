from flask import Blueprint, request
import conf
from utils.db import wait_engine_response

app = Blueprint('engine', __name__)

@app.route("/request", methods=["POST"])
def send_engine_request():
    from utils.engine import send_request
    data = request.get_json()
    id_req = send_request(data)
    if conf.DEBUG: print("Sended request:", data,flush=True)
    resp = wait_engine_response(id_req)
    if resp is None:
        return {"status":False,"error":"No data found"}
    del resp["_id"]
    return {"status":True,"data":resp}
