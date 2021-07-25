
from flask import Blueprint, json, redirect, Response
import conf
from utils import db

app = Blueprint('config', __name__)

def get_json_donwload(data,filename):
    return Response(json.dumps(data), 
            mimetype='application/json',
            headers={'Content-Disposition':f'attachment;filename={filename}'})


@app.route("/download")
def donwload_state():
    if conf.APP_STATUS == "init":
        if db.getInitState() == 5:
            return get_json_donwload(db.get_config_dict(),"CTFsub_configs.json")
    else:
        return get_json_donwload(db.get_config_dict(),"CTFsub_configs.json")
    return redirect("/")