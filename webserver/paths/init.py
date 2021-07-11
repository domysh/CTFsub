
from flask import Blueprint, redirect, render_template

app = Blueprint('app', __name__)


@app.route("/<id_init>")
def start_page(id_init):
    try:
        id_init = int(id_init)
    except:
        return redirect("/")
    return render_template(f"init/init{id_init}.html",
        title="Config",
        description="Inizializzazione CTFsub"
    )
