#! /bin/python3
from utils import *
import db

class Inithandler(SKHandler):
    def mode_changed(self,data):
        self._stop()
    def flag_submit_test(self,data):
        from submitter import emulate_flag_submit
        return emulate_flag_submit(
            texts=data["text"],
            code=data["code"],
            filter_regex=data["regex"] if "regex" in data else None,
            multiple_submit=data["multiple_submit"],
            max_submit=data["max_submit"] if data["multiple_submit"] else None,
            send_duplicate=data["duplicate"]
        )
    def pip_install(self, data):
        return install_libs(data["libs"])

class Handler(SKHandler):
    def pip_install(self, data):
        return install_libs(data["libs"])
    def flag_submit_test(self,data):
        from submitter import emulate_flag_submit
        return emulate_flag_submit(
            texts=data["text"],
            code=data["code"],
            filter_regex=data["regex"] if "regex" in data else None,
            multiple_submit=data["multiple_submit"],
            max_submit=data["max_submit"] if data["multiple_submit"] else None,
            send_duplicate=data["duplicate"]
        )
    def mode_changed(self,data):
        #Advice The submitter and the attacker about the new configs
        pass

def main():
    db.init()
    while db.get_settings()["mode"] == "init":
        Inithandler()
    if conf.DEBUG: print("Engine setted in running mode!", flush=True)
    init_modules()
    Handler()
    wait_modules()

if __name__ == '__main__': main()

