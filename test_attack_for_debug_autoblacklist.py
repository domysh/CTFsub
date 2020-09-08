from utils.classes import *
##########################################################
#                Write here your code
##########################################################
#This is the address that the program use while testing
IP_ADDRESS_DEBUG = "10.10.1.1"

# 'main' function
def run(ip,log,g_var):
    from time import sleep
    from random import randint as rnd
    g_var_set(g_var,'count',0)
    if ip == "10.10.7.1":
        raise Exception('lol')
    sleep(rnd(2,10)) #Simulating work
    
    log.info(f"Success! Test g_var status: {g_var['count']}")
    g_var['count'] +=1
    
    return ['flg{aaaaaaaaaaaaaaaaaaaaaaaaa}',
    'flag2{aaaaaaaaaaaaabbaaaaaaaaaa}',
    'a long string that may contain a flag but in this case NOPE']


'''
Insert here the port of the service if you want a control
of his status (if the service not responde skip the ip)
if active_ctrl is None or you remove CONFIG, CTFsub will skip this
control (You can segnal off status of the service raising AttackRequestRefused())
'''
CONFIG = {
    'alive_ctrl':None,
    'on':True,
    'timeout':5
}

"""
if you are in the situation that you have to 
send a signal for say that the vuln is closed use:
raise AttackFailed()

Instead if you want comunicate that the service is closed:
raise AttackRequestRefused()

When you have to full the array, remember that you can insert into it also 
long strings containing the flag (or more flag), before submitting all flags are filtered

for using g_vars, inizialize tham using:  
g_var_set(g_var,name_of_var,start_val)

than use it as a dict:
g_var[name] = var
or
function(g_var[var_to_pass])
"""

##########################################################
#                    End code part
##########################################################

#Ignore code under this comment

global ATTACK
if __name__ == '__main__':
    import logging, os, json
    if not os.path.exists('tmp.file.json'): open('tmp.file.json','wt').write('{}')
    dic_perm = json.loads( open('tmp.file.json','rt').read() )
    print('After testing please remove "tmp.file.json"')
    exce = None
    try:
        logging.basicConfig(format='LOG: %(message)s',level=logging.INFO)
        print("Result: ", run(IP_ADDRESS_DEBUG,logging.getLogger(__name__), dic_perm) )
    except Exception as e:exce = e
    open('tmp.file.json','wt').write(json.dumps(dic_perm))
    if not exce is None:
        raise exce 
else:
    global ATTACK
    ATTACK = utils.classes.AttackModel(run)

    
