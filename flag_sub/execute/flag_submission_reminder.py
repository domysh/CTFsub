
from enum import Enum
class SubmitStatus(Enum):
    SUCCESS = 0
    FAILED = 1
    INVALID = 2

input_code = """
#Example of implementation:
import requests
try:
    status = requests.get("https://google.com").status_code
    if status != 200:
        if status == 429:
            STATUS = FAILED #Too many requests to game server
        elif status == 400:
            STATUS = INVALID #The flag submitted is not a valid flag
    
except requests.exceptions.Timeout: #Probably the gameserver isn't up
    STATUS = FAILED
"""

locals_vars = {
    "FLAG":"flg{flag_to_send}",
    "STATUS":SubmitStatus.SUCCESS,
    "SUCCESS":SubmitStatus.SUCCESS,
    "FAILED":SubmitStatus.FAILED,
    "INVALID":SubmitStatus.INVALID
}

def dummy_function(*args,**kargs):pass
exec(input_code, {"exit":dummy_function,"quit":dummy_function}, locals_vars)

result = locals_vars["STATUS"]

print(result)




