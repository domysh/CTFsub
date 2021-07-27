from flask import Blueprint, session, current_app 
from werkzeug.utils import redirect
import conf
from utils import db
from . import init, config, engine


app = Blueprint('api', __name__)

app.register_blueprint(init.app, url_prefix="/init")
app.register_blueprint(config.app, url_prefix='/config')
app.register_blueprint(engine.app, url_prefix='/engine')

@app.route("/allow_single_access")
def give_single_access():
    current_app.config["ALLOWED_SESSION_SINGLE_ACCESS"] = session["id"]
    conf.SKIO.emit("reload-page", {}, broadcast=True)
    return redirect("/")


@app.route("/back_to_configuration")
def back_to_conf():
    db.set_config_mode()
    current_app.config["ALLOWED_SESSION_SINGLE_ACCESS"] = session["id"]
    conf.SKIO.emit("reload-page", {}, broadcast=True)
    return redirect("/")



@app.route("/single_access")
def have_single_access():
    return {"status":current_app.config["ALLOWED_SESSION_SINGLE_ACCESS"] == session["id"]}