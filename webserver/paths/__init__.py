from flask import Blueprint, render_template
from . import api, init
app = Blueprint('app', __name__)

app.register_blueprint(api.app, url_prefix='/api')
app.register_blueprint(init.app, url_prefix='/init')

@app.route("/")
def home_ctfsub():
    return render_template("home.html", description="CTFsub attacker")

@app.route("/addattack")
def add_attack():
    return render_template("addattack.html", description="CTFsub attacker")