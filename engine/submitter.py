import traceback
import utils, re, conf

def submitter():
    print("Submitter - Started!")

def send_flag(row_data, settings):
    pass

from enum import Enum
class SubmitStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    INVALID = "INVALID"

def submit_execute(code,flg):
    import traceback
    from io import StringIO
    from contextlib import redirect_stdout, redirect_stderr
    locals_vars = {
        "FLAG":flg,
        "STATUS":SubmitStatus.FAILED,
        "SUCCESS":SubmitStatus.SUCCESS,
        "FAILED":SubmitStatus.FAILED,
        "INVALID":SubmitStatus.INVALID
    }

    def dummy_function(*args,**kargs): return None

    exec_out = StringIO()
    with redirect_stdout(exec_out):
        with redirect_stderr(exec_out):
            try:
                exec(code, {"exit":dummy_function,"quit":dummy_function,"input":dummy_function}, locals_vars)
            except Exception:
                traceback.print_exc()
    exec_out = exec_out.getvalue()

    result = SubmitStatus.FAILED
    if type(locals_vars["STATUS"]) == SubmitStatus:
        result = locals_vars["STATUS"]

    return result.value,exec_out

def emulate_flag_submit(texts, code, filter_regex, multiple_submit, max_submit, send_duplicate):
    from base64 import b64decode
    flag_list = []
    try:
        if type(texts) == str:
            texts = [texts]
        elif type(texts) != list:
            if not all([type(ele) == str for ele in texts]):
                return {"status":False,"error":"Invalid text input"}
        flag_list = [b64decode(ele) for ele in texts]
        if not filter_regex is None:
            if type(filter_regex) != bytes:
                filter_regex = filter_regex.encode()
            if utils.check_valid_regex(filter_regex):
                flag_new_list = []
                for ele in flag_list:
                    flag_new_list += re.findall(filter_regex,ele)
                flag_list = flag_new_list
            else:
                return {"status":False,"error":"Invalid regex"}
    except (ValueError, TypeError):
        return {"status":False,"error":"Invalid base64 data"}
    if not send_duplicate:
        flag_list = list(set(flag_list))
    
    to_submit = None
    if multiple_submit:
        if type(max_submit) != int or max_submit < 1:
            return {"status":False,"error":"Invalid Max Submit Value"}
        to_submit = []
        for ele in flag_list[:max_submit]:
            try:
                to_submit.append(ele.decode())
            except UnicodeDecodeError:
                pass
    else:
        flag_list = [ele for ele in flag_list if ele]
        if len(flag_list) > 0:
            try:
                to_submit = flag_list[0].decode()
            except UnicodeDecodeError:
                pass

    if not to_submit:
        return {"status":False,"error":"No flag detected to send"}

    if not utils.is_valid_python(code):
        return {"status":False,"error":"Python code have syntax errors!"}
    try:
        return {"status":True,"result":submit_execute(code,to_submit)}
    except Exception as e:
        if conf.DEBUG: traceback.print_exc()
        return {"status":False,"error":"Unexpected error: "+str(e)}






