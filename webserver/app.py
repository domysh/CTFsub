from flask import Flask, redirect, request, render_template, session
from datetime import timedelta
from utils.db import getInitState, get_settings
import conf, os, paths, secrets
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = os.urandom(32) #This will change at every restart
                                # A reboot could reset config only in configuration process
#This website haven't to be accessed by other teams (Thay would execute python code arbitrary)!
app.config['BASE_URL'] = "http://localhost:5050/"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=365)
app.debug = conf.DEBUG
app.config["ALLOWED_SESSION_SINGLE_ACCESS"] = None

conf.SKIO = SocketIO(app)

app.register_blueprint(paths.app)

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")

@app.before_first_request
def initial_operations():
    conf.APP_STATUS = get_settings()["mode"]

@app.before_request
def prev_action():
    if "id" not in session:
        session["id"] = secrets.token_hex(32)
    if conf.APP_STATUS == "init" and not request.path.startswith("/static/"):
        if app.config["ALLOWED_SESSION_SINGLE_ACCESS"] is None:
            app.config["ALLOWED_SESSION_SINGLE_ACCESS"] = session["id"]
        if app.config["ALLOWED_SESSION_SINGLE_ACCESS"] != session["id"]:
            if request.path == "/api/allow_single_access" or request.path == "/api/single_access":
                pass
            elif request.path.startswith("/api/"):
                return redirect("/")
            else:
                return render_template("single_access_required.html",
                    title="One Access allowed!",
                    description="During the configuration only one browser is allowed"
                )
        elif not request.path.startswith("/api/"): #Init status
            state = getInitState()
            if request.path != f"/init/{state}":
                return redirect(f"/init/{state}") #Automatic redirect
    if conf.APP_STATUS == "run":
        if request.path.startswith("/init/"):
            return redirect("/")

if __name__ == "__main__":
    conf.SKIO.run(app, host="0.0.0.0",port=9999,debug=conf.DEBUG)

