from flask import Flask, redirect, request, render_template
from datetime import timedelta
from utils.db import getInitState
import conf, os, paths

app = Flask(__name__)
app.secret_key = os.urandom(32) #This will change at every restart
                                # A reboot could reset config only in configuration process
#This website haven't to be accessed by other teams (Thay would execute python code arbitrary)!
app.config['BASE_URL'] = "http://localhost:5050/"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=365)
app.debug = True

app.register_blueprint(paths.app)

@app.before_first_request
def initial_operations():
    from utils.db import create_indexes, get_settings, create_settings
    create_indexes()
    create_settings() 
    conf.APP_STATUS = get_settings()["mode"]

@app.before_request
def prev_action():
    if not request.path.startswith("/api/") and conf.APP_STATUS == "init": #Init status
        state = getInitState()
        if request.path != f"/init/{state}":
            return redirect(f"/init/{state}") #Automatic redirect

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=9999)
