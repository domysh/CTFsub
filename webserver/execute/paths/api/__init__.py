from flask import Blueprint, make_response, jsonify
from . import init, flag_submit_code
import conf
from utils.db import get_flag_submit_code

app = Blueprint('api', __name__)

app.register_blueprint(init.app, url_prefix="/init")
app.register_blueprint(flag_submit_code.app, url_prefix='/flag-submit-code')

