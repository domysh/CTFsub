import re, ast

def get_syntax_errors(code):
    try:
        ast.parse(code)
    except SyntaxError:
        import traceback
        return traceback.format_exc()
    return None
 
def check_valid_regex(r):
    try:
        re.compile(r)
        return True
    except re.error:
        return False

def check_ip(Ip):
    ip_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    return re.search(ip_regex, Ip)