from flask import Blueprint, json, request, jsonify
from . import init, flag_submit_code
import conf
from utils.db import get_engine_response

app = Blueprint('api', __name__)

app.register_blueprint(init.app, url_prefix="/init")
app.register_blueprint(flag_submit_code.app, url_prefix='/flag-submit-code')

@app.route("/engine/request", methods=["POST"])
def send_engine_request():
    from utils.engine import send_request
    data = request.get_json()
    id_req = send_request(data)
    if conf.DEBUG: print("Sended request:", data,flush=True)
    return jsonify({"id":id_req})

@app.route("/engine/response/<req_id>")
def get_engine_response_api(req_id):
    resp = get_engine_response(req_id)
    if resp is None:
        return jsonify({"status":False,"error":"No data found"})
    del resp["_id"]
    return jsonify({"status":True,"data":resp})

