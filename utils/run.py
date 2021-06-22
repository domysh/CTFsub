#!/usr/bin/python3
'''

CTFsub(mitter) for CTF A/D

Author: DomySh (Domingo Dirutigliano)
Contact: me@domysh.com
Website: www.domysh.com

'''
try:
    import utils
except:
    exit("Utils not founed!")
try:
    from utils.config import GLOBAL_LOG_FILE
except Exception as e:
    exit("Failed to import PATH to logs from config: "+str(e))

try:
    import multiprocessing, time, threading
    import importlib, re, sys, os
    from time import sleep
    from syjson import SyJson
except Exception as e:
    exit("Failed to import some libraries: "+str(e))

try:
    from utils.classes import Attacker, FlagSubmitFailed, WrongFlagSubmit
except Exception as e:
    exit("Failed to import Attacker class: "+str(e))

try:
    from utils.config import GLOBAL_DATA_FILE, GLOBAL_SETTINGS_FILE, FLAG_REGEX, flag_submit, ATTACK_PKG
    from utils.config import SHELL_CAN_USE, TIMES_TO_BLACKLIST, ATTACKS_FOLDER, TIMEOUT_ATTACK
    from utils.config import THREADING_LIMIT, AUTO_BLACKLIST_ON, TIME_TO_WAIT_IN_BLACKLIST, TICK_TIME, TEAMS_LIST
    from utils.config import SUBMIT_DUPLICATED_FLAGS, MULTIPLE_FLAG_SUBMIT, MAX_FLAG_SUBMIT, FLAG_SUBMISSION_TIME_LIMIT
except Exception as e:
    exit("Failed to import some configs: "+str(e))

try:
    log = utils.fun.setup_logger('CTFsub', GLOBAL_LOG_FILE)
except Exception as e:
    exit("Failed to create log objects: "+str(e))
#global vars synced with relative files
class glob: 
    constant_vars = SyJson(GLOBAL_DATA_FILE, get_primitives = True)
    settings = SyJson(GLOBAL_SETTINGS_FILE, get_primitives = True)
    break_wait_time = False
    break_round_attacks = False
    flag_submit_access = threading.Lock() #Manage flag_submit between flags
    last_sumbission_time = 0

def timed_submit(flag):
    if not FLAG_SUBMISSION_TIME_LIMIT is None and FLAG_SUBMISSION_TIME_LIMIT > 0:
        while True:
            wait_seconds = glob.last_sumbission_time - time.time()
            if wait_seconds >= FLAG_SUBMISSION_TIME_LIMIT:
                glob.last_sumbission_time = time.time()
                break
        sleep(.1)
    flag_submit(flag)

#Function used for submit a flag
def submit_flag(flags_inp:list,regex):
    flags = []
    if not regex is None:
        #Filtering all recived flags
        for ele in flags_inp:
            try:
                if type(ele) == bytes:
                    res = re.findall(regex.encode(),ele)
                    flags += [ele.decode() for ele in res]
                else:
                    flags += re.findall(regex,ele) 
            except Exception as e:
                log.error(f'Flag filter using regex {regex} failed! You maybe losting flags for a malconfigured REGEX')
                log.exception(e)
    else:
        for ele in flags_inp:
            if type(ele) == str:
                flags.append(ele)
            elif type(ele) == bytes:
                flags.append(ele.decode())

    glob.flag_submit_access.acquire() #Critical Zone
    
    glob.settings.create("failed_flags",[])
    flags = list(set(glob.settings["failed_flags"].var()+flags))
    glob.settings["failed_flags"] = []
    if MULTIPLE_FLAG_SUBMIT:
        first_limit = 0
        loop_iterator = list(range(MAX_FLAG_SUBMIT,len(flags)+1,MAX_FLAG_SUBMIT))
        if loop_iterator[-1] != len(flags): loop_iterator.append(len(flags))
        for last_limit in loop_iterator:
            flag_packet = flags[first_limit:last_limit]
            try:
                if not SUBMIT_DUPLICATED_FLAGS:
                    flag_packet = [ele for ele in flag_packet if not utils.fun.is_duplicated(ele)]
                if len(flag_packet) > 0:
                    timed_submit(flag_packet)
                    for ele in flag_packet: utils.fun.insert_flag(ele)
                    log.info(f'Flags submitted to gameserver "{flag_packet}"')
            except WrongFlagSubmit:
                log.warning(f'Wrong flag segnalated "{flag_packet}"')
            except FlagSubmitFailed:
                log.warning(f'Flags "{flag_packet}" submit failed... submit will be retried')
                glob.settings["failed_flags"] = glob.settings["failed_flags"].var() + flag_packet
            except Exception as e:
                log.error(f'Submission of "{flag_packet}" flag, FAILED!')
                glob.settings["failed_flags"] = glob.settings["failed_flags"].var() + flag_packet
                log.exception(e)
            first_limit = last_limit
        
    else:
        for flag in flags:
            try:
                if SUBMIT_DUPLICATED_FLAGS or not utils.fun.is_duplicated(flag):
                    timed_submit(flag)
                    utils.fun.insert_flag(flag)
                    log.info(f'Flag submitted to gameserver "{flag}"')
            except WrongFlagSubmit:
                log.warning(f'Wrong flag segnalated "{flag}"')
            except FlagSubmitFailed:
                log.warning(f'Flag "{flag}" submit failed... submit will be retried')
                glob.settings["failed_flags"].append(flag)
            except Exception as e:
                log.error(f'Submission of "{flag}" flag, FAILED!')
                glob.settings["failed_flags"].append(flag)
                log.exception(e)
    glob.flag_submit_access.release() #Critical Zone - END

#Get python module file of the attack and use it
def get_attack_by_name(attack_name,cache_use = False):
    res = getattr(__import__(f"{ATTACK_PKG}.{attack_name}"),attack_name)
    if not cache_use:
        res = importlib.reload(res) #You you change the program this will change instantly
    return res

def shell_request_manage():
    try:
        if 'shell_req' in glob.settings.keys():
            req = glob.settings['shell_req']
            if 'wait_for' in req.keys():
                if req['wait_for'] == 'sub':
                    try:
                        if shell_reqest_dispatcher(req['id_req'],req):
                            req['wait_for'] = 'shell'
                        else:
                            glob.settings['shell_req'] = {}
                    except Exception as e:
                        log.error('Failed to execute shell requests')
                        log.exception(e)
                elif req['wait_for'] is None:
                    glob.settings['shell_req'] = {}

    except Exception as e:
        log.error('Failed to read shell requests')
        log.exception(e)

def shell_reqest_dispatcher(action,req_dict):
    if action == 'break-wait-time':
        if not glob.break_wait_time:
            log.info('Requested from shell to skip wait time for this round')
            glob.break_wait_time = True
    elif action == 'stop-attacks':
        if not glob.break_round_attacks:
            log.info('Requested from shell to stop attacks for this round')
            glob.break_round_attacks = True
    elif action == 'config':
        if req_dict['operation_type'] == 'get':
            config_name = req_dict['target_key']
            if config_name in SHELL_CAN_USE:
                req_dict['response_value'] = getattr(utils.config, config_name)
                return True
        elif req_dict['operation_type'] == 'set':
            config_name = req_dict['target_key']
            if config_name in SHELL_CAN_USE:
                setattr(utils.config, config_name, req_dict['target_value'])
                log.info(f'utils.config.{config_name} assigned to {req_dict["target_value"]}')
        elif req_dict['operation_type'] == 'list':
            names = SHELL_CAN_USE
            values = []
            for name in names:
                values.append(getattr(utils.config, name))
            req_dict['response_values'] = values
            req_dict['response_names'] = names
            return True

    else:
        log.info('Unrecognised shell request... skipping')
    return None

#Thread function that have to execute a function
def start_attack(py_attack, assigned_ip):
    #Starting the attack...
    set_stdstreams()
    try:
        attack_file = get_attack_by_name(py_attack)
        if "run" not in dir(attack_file) or not callable(attack_file.run):
            log.error(f'{py_attack} haven\'t a run function... please insert it! ... skipping')
            return
        #Import the file and importing an Istance of the Attack Class
        this_attack = Attacker(attack_file.run)
        this_attack.attack_name = utils.fun.min_name(py_attack)

        #Get the flag and submit
        flags_obtained = 'leak_closed'

        #Get attack settings
        attack_settings = glob.settings['process_controller'][py_attack]

        #Managing alive control for the remote service
        if not (attack_settings['alive_ctrl'] is None):
            #if wanted as decribed in the attack file, we control first if the service is on
            if not utils.fun.is_port_in_use(assigned_ip,attack_settings['alive_ctrl']):
                log.warning(f'We found closed port attacking {assigned_ip}:{attack_settings["alive_ctrl"]} with {py_attack} attack')
                return

        #Queue for get the result from Process used for put a TIMEOUT at the attack
        res = multiprocessing.Queue()

        var_dict = glob.constant_vars[this_attack.attack_name][assigned_ip].var()
        # choose what timeout time to use
        timeout_process = TIMEOUT_ATTACK
        if not attack_settings['timeout'] is None:
            timeout_process = attack_settings['timeout']

        #Start the process
        p = multiprocessing.Process(target=this_attack.get_flags,args=(assigned_ip, var_dict, res))
        p.start()
        p.join(timeout_process)

        # If thread is still active we kill it
        if p.is_alive():
            log.info(f'{py_attack} on {assigned_ip} This thread taked over {timeout_process} seconds, killing...')
            p.terminate()
            p.join()
        else:
            #get the result (sending the flag and saving changes of permanent vars)
            flags_obtained = res.get()
            glob.constant_vars[this_attack.attack_name][assigned_ip].sync(res.get())
        
        del this_attack
        
        #Updating the status of auto blacklist
        blacklist_status = glob.settings['blacklist'][py_attack][assigned_ip]

        if flags_obtained is None or flags_obtained == 'leak_closed':
            #If this attack is a try to re-attack a team that probably have closed the vuln
            if blacklist_status['stopped_times'] == -1 and blacklist_status['excluded']:
                blacklist_status['stopped_times'] = 0
            else:
                #Count fail time, if it fails enougth times, we put it in the auto blacklist
                blacklist_status['fail_times'] += 1
                if blacklist_status['fail_times'] >= TIMES_TO_BLACKLIST:
                    #Start auto blacklist
                    blacklist_status['excluded'] = True
                    blacklist_status['stopped_times'] = 0


        #Send a different message on log for different situations
        if flags_obtained is None: # Unexpected error
            log.error(f'unexpected error attacking {assigned_ip} using {py_attack} attack have been raised')
        elif flags_obtained == 'leak_closed': #Attack failed (Because the leak is closed)
            log.warning(f'Attack to {assigned_ip} using {py_attack} attack FAILED (leak closed)!')
        elif flags_obtained == 'service_closed': # Service not reponding or take lot's of time
            log.warning(f'Find closed service to {assigned_ip} using {py_attack} attack !')
        else:
            # if the attack went successfully send the flag and reset blacklist status (Usefull for an attack reopened)
            blacklist_status.sync({
                    'excluded':False,
                    'fail_times':0,
                    'stopped_times':0
            })
            if attack_settings['custom_regex'] == False:
                submit_flag(flags_obtained,None)
            elif type(attack_settings['custom_regex']) == str:
                submit_flag(flags_obtained,attack_settings['custom_regex'])
            else:
                submit_flag(flags_obtained,FLAG_REGEX)

            
    #Fail case (return result form attack script isn't what we expected)
    except Exception as e:
        log.error(f'An unexpected result recived on {assigned_ip} using {py_attack} attack... continuing')
        log.exception(e)

def get_attack_file_list():
    wait_for_attacks = False
    to_exec = []
    while True:  
        #Taking the list of the python executable to run for the attack
        to_exec = [f for f in utils.fun.get_pythonfile_list(ATTACKS_FOLDER) if f != '__init__'] 
        if len(to_exec) == 0:
            if wait_for_attacks == False:
                log.info('Waiting for attacks python files')
                wait_for_attacks = True
            time.sleep(.1)
        else:
            if wait_for_attacks == True:
                log.info('Python attack file found! STARTING...')
            break
    return to_exec

def init_setting_section():
    if 'blacklist' not in glob.settings.keys():
        glob.settings['blacklist'] = {}

    if 'process_controller' not in glob.settings.keys():
        glob.settings['process_controller'] = {}

def init_settings_for_attack(py_file):
    if py_file not in glob.settings['blacklist'].keys():
        glob.settings['blacklist'][py_file] = {}
    
    if py_file not in glob.settings['process_controller'].keys():
        glob.settings['process_controller'][py_file] = {
            'alive_ctrl':None,
            'on':True,
            'whitelist_on':False,
            'excluded_ip':[],
            'whitelist_ip':[],
            'timeout':None,
            'custom_regex':None
        }
        # Try to charge all specific configs from the attack file
        
    atk = get_attack_by_name(py_file)
    if 'PORT' in dir(atk) and not atk.PORT is None and type(atk.PORT) == int:
        glob.settings['process_controller'][py_file]['alive_ctrl'] = atk.PORT
    
    if 'TIMEOUT' in dir(atk) and not atk.TIMEOUT is None and type(atk.TIMEOUT) in (int,float):
        glob.settings['process_controller'][py_file]['timeout'] = atk.TIMEOUT

    if ('BLACKLIST' in dir(atk) and 'WHITELIST' in dir(atk)):
        log.warning(f"found in {py_file} BLACKLIST and WHITELIST together... No option setted!")
        return

    if 'BLACKLIST' in dir(atk) and type(atk.BLACKLIST) == list:
        glob.settings['process_controller'][py_file]['whitelist_on'] = False
        glob.settings['process_controller'][py_file]['excluded_ip'] = atk.BLACKLIST
    
    if 'WHITELIST' in dir(atk) and type(atk.WHITELIST) == list:
        glob.settings['process_controller'][py_file]['whitelist_on'] = True
        glob.settings['process_controller'][py_file]['whitelist_ip'] = atk.WHITELIST

    if 'FLAG_REGEX' in dir(atk):
        if type(atk.FLAG_REGEX) in (str,bytes):
            if type(atk.FLAG_REGEX) == bytes: atk.FLAG_REGEX = atk.FLAG_REGEX.decode()
            glob.settings['process_controller'][py_file]['custom_regex'] = atk.FLAG_REGEX
        elif atk.FLAG_REGEX is None:
            glob.settings['process_controller'][py_file]['custom_regex'] = False

def clear_not_in_list(atk_list):
    for key_ele in glob.settings['process_controller'].keys():
        if key_ele not in atk_list:
            del glob.settings['process_controller'][key_ele]
            if key_ele in glob.settings['blacklist'].keys():
                del glob.settings['blacklist'][key_ele]

def set_stdstreams():
    f_tmp = open(os.devnull, 'r')
    sys.stdin = f_tmp
    f_tmp = open(os.devnull, 'w')
    sys.stout = f_tmp
    f_tmp = open(os.devnull, 'w')
    sys.sterr = f_tmp

def main():
    set_stdstreams()
    utils.fun.db_init()
    log.info('CTFsub is starting !')
    init_setting_section()
    while True:
        attack_list = get_attack_file_list()

        clear_not_in_list(attack_list)
        
        #Get start time for calculating at the end of the attack how many time have to wait
        last_time = time.time()
        # Start the round
        log.info('Round Started')
        thread_list = []
        for py_f in attack_list: #Starting attacks ! 
            try:
                init_settings_for_attack(py_f)
            except:
                log.critical(f"Error in initialize settings of attack {py_f} ... skipping!")
                continue

            log.info(f'STARTING {py_f} attack!')

            for ip_to_attack in TEAMS_LIST:  

                #break attack if requested
                if glob.break_round_attacks:break 
                
                #Wait for a free thread following the THREADING_LIMIT
                while len(thread_list) >= THREADING_LIMIT:
                    #Wait for a free thread
                    shell_request_manage()    
                    for i in range(len(thread_list)):
                        if not thread_list[i].is_alive():
                            thr = thread_list.pop(i); del thr
                            break
                    time.sleep(.1)

                if ip_to_attack not in glob.settings['blacklist'][py_f].keys():
                    glob.settings['blacklist'][py_f][ip_to_attack] = {
                        'excluded':False,
                        'fail_times':0,
                        'stopped_times':0
                    }

                attack_blacklist = glob.settings['blacklist'][py_f][ip_to_attack]
                attack_settings = glob.settings['process_controller'][py_f]
                

                #Choose what action do following the istruction in settings dict
                if attack_settings['on']: # If the attack is enabled
                    #Control list controls
                    if attack_settings['whitelist_on']: #Filtering with blacklist or withlist
                        #Filter whitelist
                        if ip_to_attack not in attack_settings['whitelist_ip']:
                            continue
                    else:
                        #Filter blacklist
                        if ip_to_attack in attack_settings['excluded_ip']:
                            log.warning(f'{py_f} attack on IP {ip_to_attack} in blacklist... skipping')
                            continue
                    #Auto blacklist control
                    if AUTO_BLACKLIST_ON:
                        if attack_blacklist['excluded']:
                            if attack_blacklist['stopped_times'] == -1:
                                pass # Last time the service was closed so we have to try again to attack
                            if attack_blacklist['stopped_times'] >= TIME_TO_WAIT_IN_BLACKLIST:
                                log.warning(f'auto_blacklist enabled on ip {ip_to_attack} of {py_f} attack ... trying anyway to execute')
                                attack_blacklist['stopped_times'] = -1 # If success -1 remember to reset blacklist
                            else:
                                log.warning(f'auto_blacklist enabled on ip {ip_to_attack} of {py_f} attack ... skipping')
                                attack_blacklist['stopped_times'] += 1
                                continue
                else:
                    log.warning(f'{py_f} attack disabilited! Skipping...')
                    break
                
                #Set up structure for save permanent vars
                if py_f not in glob.constant_vars.keys():
                    glob.constant_vars[py_f] = {}
                    glob.constant_vars[py_f][ip_to_attack] = {}
                elif ip_to_attack not in glob.constant_vars[py_f].keys():
                    glob.constant_vars[py_f][ip_to_attack] = {}

                #Starting new thread for attack
                log.info(f'Starting thread {py_f} attack for {ip_to_attack}')
                thread_list.append(threading.Thread(target=start_attack,args=(py_f,ip_to_attack)))
                thread_list[-1].daemon = True
                thread_list[-1].start()

            log.info(f'{py_f} attack, finished!')
            if glob.break_round_attacks:break #break attack as requested
            
        #Wait for threads work finish
        log.info('Waiting for thread work finish')
        if glob.break_round_attacks: glob.break_round_attacks = False #Attack breaked!
        while len(thread_list) != 0:
            #Wait for a free thread
            time.sleep(.1)
            shell_request_manage()
            for i in range(len(thread_list)):
                if not thread_list[i].is_alive():
                    thr = thread_list.pop(i); del thr
                    break
        del thread_list
        log.info(f'Attacks for this round finished')

        #Wait remaing time
        time_to_wait = TICK_TIME - (time.time() - last_time)
        if time_to_wait > 0:
            log.info(f'{int(time_to_wait//60)} minutes and {int(time_to_wait)%60} seconds for new round')
            while time_to_wait > 0:
                time_to_wait = TICK_TIME - (time.time() - last_time)
                shell_request_manage()
                if glob.break_wait_time:
                    glob.break_wait_time = False
                    break
                sleep(.1)

    
