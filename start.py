import requests, os, logging, re, json
import multiprocessing, time, threading
from multiprocessing import Pool
import utils.config, utils.fun
from time import sleep


#Creating the logger

log = utils.fun.setup_logger('CTFsub',utils.config.GLOBAL_LOG_FILE)
flag_log = utils.fun.setup_logger('flags',utils.config.GLOBAL_FLAG_FILE,'%(asctime)s FLAG: %(message)s')
'''
{

#Shell Commands

requests:{
    what:"Cacca"
    params:"..."
    "taked":False / True
    response{
        what:"LOL"
        "listened":False/True
    }

}

# shell -> settings.json -> CTFsub -> settings.json -> shell -> settings.json <delete--- CTFsub
config:{
    AAAA = BBBB
}
}
'''
class glob: 
    constant_vars = {}
    commit_lock = threading.Lock()
    settings = {}
    settings_lock = threading.Lock()

def commit_vars_changes():
    glob.commit_lock.acquire()
    open(utils.config.GLOBAL_DATA_FILE,'wt').write(json.dumps(glob.constant_vars))
    glob.commit_lock.release()

def commit_settings():
    glob.settings_lock.acquire()
    open(utils.config.GLOBAL_SETTINGS_FILE,'wt').write(json.dumps(glob.settings))
    glob.settings_lock.release()

#Load Glob vars
fl = open(utils.config.GLOBAL_DATA_FILE,'rt').read()
if fl != "":
    glob.constant_vars = json.loads(fl)

fl = open(utils.config.GLOBAL_SETTINGS_FILE,'rt').read()
if fl != "":
    glob.settings = json.loads(fl)  

def submit_flag(flags:list):
    flags = re.findall(utils.config.FLAG_REGEX," ".join(flags)) #Filetring all recived flags
    sended = []
    for flag in flags:
        if flag not in sended:
            try:
                flag_log.info(flag)
                requests.post(utils.config.SUB_URL, data={'team_token': utils.config.TEAM_TOKEN, 'flag': flag},timeout=3)
                log.info(f'Submitted to gameserver "{flag}" flag')
                sended.append(flag)
            except Exception as e:
                log.error(f'Submission of "{flag}" flag, FAILED!, see flag log for details')
                flag_log.exception(e)
    del sended

def get_attack_by_name(attack_name):
    return getattr(__import__(f"{utils.config.ATTACK_PKG}.{attack_name}"),attack_name)

def start_attack(py_attack,assigned_ip):
    #Starting the attack...
    try:
        #Import the file and importing an Istance of the Attack Class
        this_attack = get_attack_by_name(py_attack).ATTACK
        this_attack.attack_name = utils.fun.min_name(py_attack)
        #Verify that is the sub class wanted
        if not isinstance(this_attack,utils.classes.AttackModel):
            log.error(f'{py_attack} file havent a Attack Class that is subclass of AttackModel... Skipping attack...')
            return
        #Get the flag and submit
        flags_obtained = 'service_closed'

        attack_settings = glob.settings['process_controller'][py_attack]

        if not (attack_settings['alive_ctrl'] is None):
            if not utils.fun.is_port_in_use(assigned_ip,attack_settings['alive_ctrl']):
                log.warning(f'We found closed port attacking {assigned_ip}:{attack_settings["alive_ctrl"]} with {py_attack} attack')
                return

        res = multiprocessing.Queue()

        var_dict = {}
        
        if this_attack.attack_name not in glob.constant_vars.keys():
            glob.constant_vars[this_attack.attack_name] = {}
            commit_vars_changes()
            
        if assigned_ip in glob.constant_vars[this_attack.attack_name].keys():
            var_dict = glob.constant_vars[this_attack.attack_name][assigned_ip]
        

        p = multiprocessing.Process(target=this_attack.get_flags,args=(assigned_ip, var_dict, res))
        p.start()

        # Wait for TIMEOUT TIME
        p.join(utils.config.TIMEOUT_ATTACK)

        # If thread is still active we kill it
        if p.is_alive():
            log.info(f'GLOBAL_TIMEOUT {py_attack} on {assigned_ip} finished! killing...')
            p.terminate()
            p.join()
        else:
            flags_obtained = res.get()
            glob.constant_vars[this_attack.attack_name][assigned_ip] = res.get()
            commit_vars_changes()
        
        del this_attack
        
        blacklist_status = glob.settings['blacklist'][py_attack][assigned_ip]

        if flags_obtained is None or flags_obtained == 'leak_closed':
            if blacklist_status['stopped_times'] == -1 and blacklist_status['excluded']:
                blacklist_status['stopped_times'] = 0
            else:
                blacklist_status['fail_times'] += 1
                if blacklist_status['fail_times'] >= utils.config.TIMES_TO_BLACKLIST:
                    #Start auto blacklist
                    blacklist_status['excluded'] = True
                    blacklist_status['stopped_times'] = 0

            commit_settings()


        if flags_obtained is None:
            log.error(f'unexpected error attacking {assigned_ip} using {py_attack} attack have been raised')
        elif flags_obtained == 'leak_closed': #Attack failed (Because the leak is closed)
            log.warning(f'Attack to {assigned_ip} using {py_attack} attack FAILED (leak closed)!')
        elif flags_obtained == 'service_closed':
            log.warning(f'Find closed service to {assigned_ip} using {py_attack} attack !')
        else:
            blacklist_status = {
                    'excluded':False,
                    'fail_times':0,
                    'stopped_times':0
            }
            commit_settings()
            submit_flag(flags_obtained)
            
    #Fail case (return result form attack script isn't what we expected)
    except Exception as e:
        log.error(f'An unexpected result recived on {assigned_ip} using {py_attack} attack... continuing')
        log.exception(e)

def main():
    log.info('CTFsub is starting !')
    while True:
        
        last_time = time.time()

        wait_for_attacks = False
        while True:

            to_exec = utils.fun.get_pythonfile_list(utils.config.ATTACKS_FOLDER) #Taking the list of the python executable to run for the attack
            if len(to_exec) == 0 or to_exec == ['__init__']:
                if wait_for_attacks == False:
                    log.info('Waiting for attacks python files')
                    wait_for_attacks = True
                time.sleep(.1)
            else:
                if wait_for_attacks == True:
                    log.info('Python attack file found! STARTING...')
                break

        flag_log.info('ROUND STARTED')
        log.info('Round Started')
        thread_list = []
        for py_f in to_exec: #Starting attacks !
            
            if py_f == "__init__": continue #Skip __init__.py file 

            log.info(f'STARTING {py_f} attack!')

            for team_id in range( utils.config.TEAM_IP_RANGE[0], utils.config.TEAM_IP_RANGE[1]+1): # repeating the attack for every team

                if team_id == utils.config.OUR_TEAM_ID: continue # Skiping our team
                ip_to_attack = utils.fun.get_ip_from_temp(utils.config.IP_VM_TEMP,{'team_id':team_id}) #calculating the ip
                
                
                while len(thread_list) >= utils.config.THREADING_LIMIT:
                    #Wait for a free thread
                    for i in range(len(thread_list)):
                        if not thread_list[i].is_alive():
                            print('odhjiiojsda')
                            thr = thread_list.pop(i); del thr
                            break
                    time.sleep(.1)
                

                # Controlling and creating blacklist and process_controller for every attack
                if 'blacklist' not in glob.settings.keys():
                    glob.settings['blacklist'] = {}
                
                if 'process_controller' not in glob.settings.keys():
                    glob.settings['process_controller'] = {}

                if py_f not in glob.settings['blacklist'].keys():
                    glob.settings['blacklist'][py_f] = {}

                if ip_to_attack not in glob.settings['blacklist'][py_f].keys():
                    glob.settings['blacklist'][py_f][ip_to_attack] = {
                        'excluded':False,
                        'fail_times':0,
                        'stopped_times':0
                    }
                

                if py_f not in glob.settings['process_controller'].keys():
                    glob.settings['process_controller'][py_f] = {
                        'alive_ctrl':None,
                        'on':True,
                        'whitelist_on':False,
                        'excluded_ip':[],
                        'whitelist_ip':[]
                    }
                    try:
                        atk = get_attack_by_name(py_f)
                        if 'CONFIG' in dir(atk):
                            for k_settings in glob.settings['process_controller'][py_f].keys():
                                if k_settings in atk.CONFIG.keys():
                                    glob.settings['process_controller'][py_f][k_settings] = atk.CONFIG[k_settings]
                        del atk
                    except Exception as e:
                        log.error('ERROR LOADING CONFIG FROM ATTACK')
                        log.exception(e)
                
                attack_blacklist = glob.settings['blacklist'][py_f][ip_to_attack]
                attack_settings = glob.settings['process_controller'][py_f]
                
                commit_settings()

                if attack_settings['on']:
                    #Control list controls
                    if attack_settings['whitelist_on']:
                        if ip_to_attack not in attack_settings['whitelist_ip']:
                            continue
                    else:
                        if ip_to_attack in attack_settings['excluded_ip']:
                            log.warning(f'{py_f} attack on IP {ip_to_attack} in blacklist... skipping')
                            continue
                    #Auto blacklist control
                    if attack_blacklist['excluded']:
                        if attack_blacklist['stopped_times'] == -1:
                            pass # Last time the service was closed so we have to try again
                        if attack_blacklist['stopped_times'] >= utils.config.TIME_TO_WAIT_IN_BLACKLIST:
                            log.warning(f'auto_blacklist enabled on ip {ip_to_attack} of {py_f} attack ... trying anyway to execute')
                            attack_blacklist['stopped_times'] = -1 # If success -1 remember to reset blacklist
                            commit_settings()
                        else:
                            log.warning(f'auto_blacklist enabled on ip {ip_to_attack} of {py_f} attack ... skipping')
                            attack_blacklist['stopped_times'] += 1
                            commit_settings()
                            continue
                else:
                    log.warning(f'{py_f} attack disabilited! Skipping...')
                    break
                
                

                #Starting new thread
                log.info(f'Starting thread {py_f} attack for {ip_to_attack}')
                thread_list.append(threading.Thread(target=start_attack,args=(py_f,ip_to_attack)))
                thread_list[-1].daemon = True
                thread_list[-1].start()

            log.info(f'{py_f} attack, finished!')
            
        #Wait for finish
        log.info('Waiting for thread work finish')
        while len(thread_list) != 0:
            #Wait for a free thread
            time.sleep(.1)
            for i in range(len(thread_list)):
                if not thread_list[i].is_alive():
                    thr = thread_list.pop(i); del thr
                    break
        del thread_list
        log.info(f'Attacks for this round finished')

        this_time = time.time()
        time_to_wait = utils.config.TICK_TIME - (this_time - last_time)
        if time_to_wait > 0:
            log.info(f'{int(time_to_wait//60)} minutes and {int(time_to_wait)%60} seconds for new round')
            sleep(time_to_wait) # Wait for the round
            
        # Adding SEC_SECONDS seconds for security
        for i in reversed(range(1,utils.config.SEC_SECONDS+1)):
            log.warning(f'{i} second for starting new round')
            sleep(1)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt,InterruptedError,KeyError):
        log.fatal('CTRL+C Pressed, Closing')
        print()
        exit()

    
