from flask import Blueprint
from . import init

app = Blueprint('api', __name__)

app.register_blueprint(init.app, url_prefix="/init")
