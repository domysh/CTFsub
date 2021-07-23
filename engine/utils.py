import socket, json, re, conf

class SocketCommandHandler():
    def __init__(self, address, port, max_data = 1024):
        self._sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sk.bind((address,port))
        self._sk.listen(1)
        self._start_loop = True
        self._max_data = max_data
        self._start()

    def _start(self):
        while self._start_loop:
            
            conn, _ = self._sk.accept()
            data = conn.recv(self._max_data)
            conn.close()
            if conf.DEBUG: print("Connection recived: data =>",data)
            try: data = json.loads(data)
            except json.JSONDecodeError: continue

            try:
                if type(data) == dict and type(data["type"]) == str:
                    command = data["type"]
                    del data["type"]
                    command = command.strip()
                    if command[0] != "_":
                        self._command_handle(command,data)
            except KeyError: continue
    
    def _command_handle(self,command,data):
        if command in dir(self):
            if conf.DEBUG: print(command,data)
            func = getattr(self,command)
            if callable(func):
                res = None
                try:
                    res = func(data)
                except Exception:
                    import traceback
                    traceback.print_exc()
                if "id" in data and not res is None:
                    import db
                    db.create_response(
                        data["id"], res
                    )
    
    def _stop(self):
        self._start_loop = False
        self._sk.close()


class SKHandler(SocketCommandHandler):
    def __init__(self):
        import conf
        super().__init__(conf.SOCKET_HOOK_ADDR,conf.SOCKET_HOOK_PORT,max_data=conf.MAX_DATA_HOOK)

def init_modules():
    start_attacker()
    start_submitter()

def wait_modules():
    import conf
    conf.ATTACKER.join()
    conf.SUBMITTER.join()

def start_attacker():
    from threading import Thread
    import conf, attacker
    conf.ATTACKER = Thread(target=attacker.attacker)
    conf.ATTACKER.daemon = True
    conf.ATTACKER.start()

def start_submitter():
    from threading import Thread
    import conf, submitter
    conf.SUBMITTER = Thread(target=submitter.submitter)
    conf.SUBMITTER.daemon = True
    conf.SUBMITTER.start()

def check_valid_regex(r):
    try:
        re.compile(r)
        return True
    except re.error:
        return False


def get_syntax_errors(code):
    import ast
    try:
        ast.parse(code)
    except SyntaxError:
        import traceback
        return traceback.format_exc()
    return None

def install_libs(libs):
    import subprocess, db
    libs = [ele.strip() for ele in libs.split() if ele and type(ele) == str and len(ele) > 0 and ele[0] != "-"]
    libs = [ele for ele in libs if ele]
    libs = list(set(libs))
    if len(libs) > 0:
        try:
            result = subprocess.run(["pip3","install","--user"]+libs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if result.returncode == 0:
                db.register_libraries(libs)
                return True, result.stdout
            else:
                return False, result.stdout
        except Exception as e:
            return False, "Command execution error: "+str(e)
    return False,"No valid module list"