from flask import Blueprint
from . import init, flag_submit_code, config, engine

app = Blueprint('api', __name__)

app.register_blueprint(init.app, url_prefix="/init")
app.register_blueprint(flag_submit_code.app, url_prefix='/flag-submit-code')
app.register_blueprint(config.app, url_prefix='/config')
app.register_blueprint(engine.app, url_prefix='/engine')


