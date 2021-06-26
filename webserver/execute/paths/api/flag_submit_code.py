from flask import Blueprint, jsonify, make_response
from utils.db import get_flag_submit_code

app = Blueprint('flag-submit-code', __name__)

@app.route("/get")
def get_submit_code():
    data = get_flag_submit_code()
    if data:
        data = {
            "status":True,
            "data":data
        }
    else:
        data = {
            "status":False,
            "msg":"Flag submit code not found!"
        }
    return make_response(jsonify(data), 200)
