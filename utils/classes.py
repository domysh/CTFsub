import utils, os, logging

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

        #Do the attack
        final_res = None
        try:
            log.info('STARTING ATTACK')
            result = self.fun_to_run(ip,log,self.glob_dict)
            log.info('END ATTACK')
            if type(result) is list:
                final_res = result
            else:
                final_res = [result]
        except AttackFailed as e: #in case of a closed leak
            log.info('ATTACK IMPOSSIBLE (LEAK_CLOSED)')
            log.exception(e)
            final_res = 'leak_closed' 
        except AttackRequestRefused as e: # in case the service is closed
            log.info('ATTACK IMPOSSIBLE BECAUSE THE SERVICE IS CLOSED')
            log.exception(e)
            final_res = 'service_closed'
        except Exception as e:
            log.info('ATTACK STOPPED FOR AND ERROR')
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

def g_var_set(gvar:dict,key:str,def_val):
    if key not in gvar.keys():
        gvar[key] = def_val

def run_test_case(func:callable,ip:str):
    import logging, os, json
    if not os.path.exists('tmp.file.json'): open('tmp.file.json','wt').write('{}')
    dic_perm = json.loads( open('tmp.file.json','rt').read() )
    print('After testing please remove "tmp.file.json"')
    exce = None
    try:
        logging.basicConfig(format='LOG: %(message)s',level=logging.INFO)
        print("Result: ", func(ip,logging.getLogger(__name__), dic_perm) )
    except Exception as e:exce = e
    open('tmp.file.json','wt').write(json.dumps(dic_perm))
    if not exce is None:
        raise exce
        
