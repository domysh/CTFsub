from flask import Blueprint, request, jsonify, make_response
import conf
from utils.db import get_engine_response

app = Blueprint('engine', __name__)

@app.route("/request", methods=["POST"])
def send_engine_request():
    from utils.engine import send_request
    data = request.get_json()
    id_req = send_request(data)
    if conf.DEBUG: print("Sended request:", data,flush=True)
    return make_response(jsonify({"id":id_req}),200)

@app.route("/response/<req_id>")
def get_engine_response_api(req_id):
    resp = get_engine_response(req_id)
    if resp is None:
        return make_response(jsonify({"status":False,"error":"No data found"}),200)
    del resp["_id"]
    return make_response(jsonify({"status":True,"data":resp}),200)