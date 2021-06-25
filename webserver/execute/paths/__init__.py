from flask import Blueprint
from . import api, init
app = Blueprint('app', __name__)

app.register_blueprint(api.app, url_prefix='/api')
app.register_blueprint(init.app, url_prefix='/init')

@app.route("/")
def home_ctfsub():
    pass