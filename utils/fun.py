import datetime
from utils.config import PRINT_LOGS
import os, logging, socket, ipaddress

def check_pid(pid:int):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def get_time():
    return datetime.datetime.now().strftime("%d-%m-%Y__%H_%M_%S")

def create_if_not_exist(path:str):
    if not os.path.exists(path):
        os.mkdir(path)

def create_file(file_path:str):
    if not os.path.exists(file_path):
        with open(file_path,"wt") as fl:
            fl.write('')

def is_port_in_use(ip,port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.5)
        return s.connect_ex((ip, port)) == 0

def getlist_file(path:str):
    if os.path.exists(path):
        general_list = os.listdir(path)
        res = []
        for ele in general_list:
            if not os.path.isdir(ele):
                res.append(ele)
        del general_list
        return res
    return False

def get_pythonfile_list(path:str):
    files = getlist_file(path)
    res = []
    for ele in files:
        if ele.endswith('.py'):
            res.append(os.path.basename(ele[:-3]))
    del files
    return res

def only_this_chars(a_str:str, chars:str):
    res = ''
    for ele in a_str:
        if ele in chars:
            res += ele
    return res

def get_ip_from_temp(tem:str,data:dict):
    ip = tem.split('.')
    if len(ip) != 4:
        raise Exception('Not a valid IP Temp')
    res = []
    for ele in ip:
        if ele[0] == '@':
            var = ele[1:]
            if var in data.keys():
                ele = str(data[var])
            else:
                raise Exception('Not valid data')
        filtered = only_this_chars(ele,'0123456789')
        if len(filtered) == 0:
            raise Exception('Not a valid IP Temp')
        if int(filtered) < 256:
            res.append(str(filtered))
        else:
            raise Exception('Not a valid IP Temp')
    return '.'.join(res)
            

def setup_logger(logger_name, log_file, head_f = '%(asctime)s * %(name)s - %(levelname)s: %(message)s', level=logging.INFO):

    log_setup = logging.getLogger(logger_name)
    formatter = logging.Formatter(head_f)
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    log_setup.setLevel(level)
    log_setup.addHandler(fileHandler)
    if PRINT_LOGS:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        log_setup.addHandler(streamHandler)

    return log_setup

def close_logger(log):
    handlers = log.handlers[:]
    for handler in handlers:
        handler.close()
        log.removeHandler(handler)

def min_name(name:str):
    return only_this_chars(name.lower().replace(' ','_'),"1234567890abcdefghijklmnopqrstuvwxyz_-.")

def is_valid_ip(ip:str):
    try:
        ipaddress.ip_address(ip)
        return True
    except:pass
    return False
