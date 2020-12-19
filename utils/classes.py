import utils, os, logging, sys

class Attacker():
    #Set the attack name as the file name
    def __init__(self,to_run:callable):
        self.fun_to_run = to_run
        self.attack_name = None
        

    # Function used by us for executing attack (creating the logger)
    def get_flags(self,ip:str,glob:dict, res):
        assert(self.attack_name != None) #This have to be assigned externaly
        self.glob_dict = glob
        #Verify that is a truth path
        self.ip_to_attack = ip
        
        #Generating the file_path for the log
        general_name = f"{self.attack_name}--{ip}"
        file_name = f"{general_name}.log"
        file_name = os.path.join(utils.config.LOG_FOLDER,self.attack_name,file_name)
        #Creating the logger
        utils.fun.create_if_not_exist(os.path.join(utils.config.LOG_FOLDER,self.attack_name))
        utils.fun.create_file(file_name)
        log = utils.fun.setup_logger(self.attack_name+' - '+ip,file_name,'%(asctime)s * '+self.ip_to_attack+' * %(name)s - %(levelname)s: %(message)s')

        f_tmp = open(os.devnull, 'r')
        sys.stdin = f_tmp
        sys.stdout = LogStdout(log)
        sys.stderr = LogStderr(log)

        #Do the attack
        final_res = None
        try:
            log.warning('STARTING ATTACK')
            result = self.fun_to_run(ip,self.glob_dict)
            log.warning('END ATTACK')
            if type(result) is list:
                final_res = result
            else:
                final_res = [result]
        except AttackFailed as e: #in case of a closed leak
            log.warning('ATTACK IMPOSSIBLE (LEAK_CLOSED)')
            log.exception(e)
            final_res = 'leak_closed' 
        except AttackRequestRefused as e: # in case the service is closed
            log.warning('ATTACK IMPOSSIBLE BECAUSE THE SERVICE IS CLOSED')
            log.exception(e)
            final_res = 'service_closed'
        except Exception as e:
            log.warning('ATTACK STOPPED FOR AND ERROR')
            log.exception(e)
            final_res = None
        finally:
            utils.fun.close_logger(log)
            res.put(final_res)
            res.put(self.glob_dict)
            return final_res

        raise Exception(f'Not vaild output by {self.attack_name} attack')
        


class AttackFailed(Exception):pass         #Use when the vuln is closed
class AttackRequestRefused(Exception):pass #Use when the connection to the server is impossible

class LogStdout(object):
    def __init__(self,log_obj):
        self.log_obj = log_obj
        self.readable = False

    def write(self,string):
        if len(string)==0:return
        for line in string.split('\n'):
            if len(line) == 0: continue
            self.log_obj.info(line)
    
    def flush(self,a=None):pass

class LogStderr(object):
    def __init__(self,log_obj):
        self.log_obj = log_obj
        self.readable = False

    def write(self,string):
        if len(string)==0:return
        for line in string.split('\n'):
            if len(line) == 0: continue
            self.log_obj.info(line)

    def flush(self,a=None):pass

def g_var_set(gvar:dict,key:str,def_val):
    if key not in gvar.keys():
        gvar[key] = def_val

def run_test_case(func:callable,ip:str):
    import logging, os, json
    if not os.path.exists('tmp.file.json'):
        print('After testing please remove "tmp.file.json"')
        open('tmp.file.json','wt').write('{}')
    dic_perm = json.loads( open('tmp.file.json','rt').read() )
    exce = None
    try:
        logging.basicConfig(format='LOG: %(message)s',level=logging.INFO)
        log_obj = logging.getLogger(__name__)
        f_tmp = open(os.devnull, 'r')
        sys.stdin = f_tmp
        sys.stdout = LogStdout(log_obj)
        sys.stderr = LogStderr(log_obj)
        print("Result: ", func(ip, dic_perm) )
    except Exception as e:
        exce = e
    open('tmp.file.json','wt').write(json.dumps(dic_perm))
    if not exce is None:
        raise exce
        
