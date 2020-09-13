#!/usr/bin/python3
import cmd, utils
from utils.syjson import SyJson
from utils.config import GLOBAL_SETTINGS_FILE, GLOBAL_DATA_FILE

class glob:
    try:
        g_var = SyJson(GLOBAL_DATA_FILE, create_file=False)
        settings = SyJson(GLOBAL_SETTINGS_FILE, create_file=False)
    except:
        print(('-'*30)+'\nBefore you run the shell,\nyou have to run CTFsub\n'+('-'*30))
        exit(1)

def getParamethers(line):
    #if '"' not in line:
    #    return [f for f in line.split(' ') if f != '']
    res = []
    in_str_mode = False
    last_back = False
    buff = ''
    for lett in line:
        if last_back:
            buff += lett
            last_back = False
        elif lett == '\\':
            last_back = True
        elif lett == ' ' and not in_str_mode:
            if buff != '':
                res.append(buff)
                buff = ''
        elif lett == '"' and buff == '' and not in_str_mode:
            in_str_mode = True
        elif lett == '"' and in_str_mode:
            in_str_mode = False
            res.append(buff)
            buff = ''
        else:
            buff+=lett
    if in_str_mode:
        raise InvalidCommand('no ending \'"\'')
    if buff != '':res.append(buff)
    return res            




def list_process_array():
    return [f for f in utils.fun.get_pythonfile_list(utils.config.ATTACKS_FOLDER) if f != '__init__']


def print_div():print('-'*30)

def list_process():
    print_div()
    try:
        for proc_key in glob.settings['process_controller'].keys():
            proc = glob.settings['process_controller'][proc_key]
            print(f'Name: {proc_key} - status: {bool_onoff(proc["on"])}')
    except KeyError:pass
    print_div()

def bool_onoff(v):
    if type(v) == bool:
        if v: return 'on'
        else: return 'off'
    elif type(v) == str:
        if v == 'on':return True
        elif v == 'off': return False

def get_set_gvar(attack_name,ip,key,value = None):
    if value is None:
        try:
            val_to_print = glob.g_var[attack_name][ip][key]
            print(f'Gvar on {attack_name}:{ip} [\'{key}\'] = {val_to_print}')
        except:
            print(f'Gvar on {attack_name}:{ip} [\'{key}\'] not founded!')
    else:
        try:
            original_v = value
            try:value = int(value)
            except:
                try:value = float(value)
                except:pass
            if original_v != str(value):
                value = original_v
            glob.g_var[attack_name][ip][key] = value
            print('Gvar setting, done :D')
        except:
            print(f'Gvar on {attack_name}:{ip} not founded!')

def reset_gvar(attack_name,ip=None):
    try:
        if ip is None:
            glob.g_var[attack_name] = {}
            print(f'Gvar for {attack_name} resetted!')
        else:
            glob.g_var[attack_name][ip] = {}
            print(f'Gvar for {attack_name}:{ip} resetted!')
    except:
        print(f'Gvar on {attack_name}:{ip} not founded!')

def enable_process(attack_name,set_to=None):
    try:
        if set_to is None:
            print(f'{attack_name} attack is {bool_onoff(glob.settings["process_controller"][attack_name]["on"])}')
        else:
            if set_to == 'on':
                glob.settings['process_controller'][attack_name]["on"] = True
                print(f'{attack_name} setted to on')
            elif set_to == 'off':
                glob.settings['process_controller'][attack_name]["on"] = False
                print(f'{attack_name} setted to off')
            else:
                print('Insert on or off for changing the status')
    except:
        print(f'Process controller of {attack_name} attack not founded!')

def whitelist_get_set(attack_name,*ips):
    attack_ctrl = get_process_controller(attack_name)
    if attack_ctrl is None: return
    try:
        status = attack_ctrl['whitelist_on']
        if len(ips) == 0:
            if status != True:
                print('ALLERT! The whitelist is disabilited')
            print(f'Whitelist for {attack_name} attack is =',attack_ctrl['whitelist_ip'])
        else:
            attack_ctrl['whitelist_ip'] = []
            if ips[0] != 'no_ip':
                for ip in ips:
                    if not utils.fun.is_valid_ip(ip):
                        print(f'{ip} is not a valid IP address!')
                        return 
                    attack_ctrl['whitelist_ip'].append(ip)
            attack_ctrl['whitelist_on'] = True
            print('All done :D')
    except:
        print(f'Process Controller of {attack_name} damaged !!!')

def blacklist_get_set(attack_name,*ips):
    attack_ctrl = get_process_controller(attack_name)
    if attack_ctrl is None: return
    try:
        status = attack_ctrl['whitelist_on']
        if len(ips) == 0:
            if status != False:
                print(f'ALLERT! The blacklist is disabilited')
            print(f'Blacklist for {attack_name} attack is =',attack_ctrl['excluded_ip'])
        else:
            attack_ctrl['excluded_ip'] = []
            if ips[0] != 'no_ip':
                for ip in ips:
                    if not utils.fun.is_valid_ip(ip):
                        print(f'{ip} is not a valid IP address!')
                        return 
                    attack_ctrl['excluded_ip'].append(ip)
            attack_ctrl['whitelist_on'] = False
            print('All done :D')
    except:
        print(f'Process Controller of {attack_name} damaged !!!')
            
def disable_filters(attack_name):
    return blacklist_get_set(attack_name,'no_ip') 

def get_process_controller(attack_name):
    try:
        return glob.settings['process_controller'][attack_name]
    except:
        print(f'Process Controller not found for {attack_name}')
        return None

def get_filter_status(attack_name):
    attack_ctrl = get_process_controller(attack_name)
    if attack_ctrl is None: return
    try:
        if attack_ctrl['whitelist_on']:
            print('Now is active the Whitelist')
            print(f'Here the IPs whitelisted: {attack_ctrl[f"whitelist_ip"]}') 
        else:
            array_ip = attack_ctrl[f"excluded_ip"]
            if len(array_ip) == 0:
                print('Filters are disabilited!')
            else:
                print('Now is active the Blacklist')
                print(f'Here the IPs blacklisted: {array_ip}') 
    except:
        print(f'Process controller of {attack_name} attack not founded!')

def get_set_timeout(attack_name,time = None):
    attack_ctrl = get_process_controller(attack_name)
    if attack_ctrl is None: return
    try:
        if time is None:
            res = attack_ctrl['timeout']
            if res is None:
                print('No timeout setted, using global timeout')
            elif type(res) in (int,float):
                print(f'Timeout setted to {int(res//60)}:{int(res%60)}')
            else:
                print('Error to read timeout')
        else:
            if time == 'no_time':
                attack_ctrl['timeout'] = None
                print('Timeout disabilited! using global timeout')
            else:
                try:time = int(time)
                except:
                    try:time = float(time)
                    except:pass
                if type(time) in (int,float):
                    attack_ctrl['timeout'] = time
                    print(f'Timeout changed to {int(time//60)}:{int(time%60)}')
    except:
        print(f'Process controller of {attack_name} attack not founded!')

def on_off_status_autoblacklist(attack_name,ip,on_or_off = None):
    blacklist_status = None
    try:
        blacklist_status = glob.settings['blacklist'][attack_name][ip]
    except:
        print('No auto_blacklist status founded!')
        return
    try:
        if on_or_off is None:
            print(f'Autoblacklist {bool_onoff(blacklist_status["excluded"])} for {attack_name}')
            print(f'Times execution failed sequently {blacklist_status["fail_times"]}')
            print(f'Times the process was blocked by autoblacklist sequently {blacklist_status["stopped_times"]}')
        else:
            if bool_onoff(on_or_off):
                blacklist_status['excluded'] = True
            else:
                blacklist_status['excluded'] = False
                blacklist_status['fail_times'] = 0
            print('Status Updated')
    except:
        print('Error reading autoblacklist settings')


class CTFsubShell(cmd.Cmd):

    prompt = 'CTFsub >> '
    intro = ""

    doc_header = 'Command help list'
    #misc_header = 'misc_header'
    undoc_header = 'Command with no documentation'
    ruler = '-'
    uncompleted_command = 'Uncompleted command! D:'
    '''
    When the paramether is variable we can find
    a dict -> {} full of routes

    or a custom var
    <var_type>::[var_name] # If no var_name is userd var_type name

    declared on another dict with:
    a function with the list of possibilities
    a list of possibility

    '''
    routes = {
        'process':{
            '@list':[list_process],
            'attack_name::':{
                'gvar':{
                    'get':{
                        'ip::':{
                            'gvar_arg::key':[get_set_gvar]
                        }
                    },
                    'set':{
                        'ip::':{
                            'gvar_arg::key':{
                                'val::value_to_set':[get_set_gvar]
                            }
                        }
                    },
                    'reset':{
                        'ip::':[reset_gvar],
                        'all':[reset_gvar]
                    }
                },
                'enable':{
                    'set':{'onoff::on_or_off':[enable_process]},
                    'status':[enable_process]
                },
                'filter':{
                    'whitelist':{
                        'set':{'ip_array::list_all_ip':[whitelist_get_set]},
                        'get':[whitelist_get_set]
                    },
                    'blacklist':{
                        'set':{'ip_array::list_all_ip':[blacklist_get_set]},
                        'get':[blacklist_get_set]
                    },
                    'disable':[disable_filters],
                    'status':[get_filter_status]

                },
                'status':[print], # Full status so will be builded at the end of the process command
                'timeout':{
                    'disable':[get_set_timeout,('no_time',)],
                    'set':{
                        'num::time_in_seconds':[get_set_timeout]
                        }, 
                    'status':[get_set_timeout]
                },
                'autoblacklist':{
                    'ip::':{
                        'set':{
                            'onoff::on_or_off':[on_off_status_autoblacklist]
                        }, 
                        'status':[on_off_status_autoblacklist] 
                    }
                },
                'alive-ctrl':{
                    'on':{
                        'intnum::port':[print] 
                    },
                    'off':[print], 
                    'status':[print] 
                }

            }
        },
        'config':{
            'list': [print], 
            'get':{
                'config_name::':[print] 
            },
            'set':{
                'config_name::':{
                    'val::value_to_set':[print] 
                }
            }
        },
        'log':{
            'print':{
                'intnum::num_of_lines':{
                    'log_name::':[print]
                },
                'all':{
                    'log_name::':[print]
                }
            },
            'reset':{
                'log_name::':[print]
            },
            'watch':{
                'log_name::':[print]
            }
        },
        'attack':{
            'async':{
                'run':{
                    'attack_name::':{
                            'ip::':[print],
                            'all':[print]
                        }
                },
                'stop':[print]
            },
            'sync':{
                'stop':[print],
                'start':[print]
            }
        }

    }



    hint_vars = {
        'attack_name':list_process_array,
        'config_name':['FLAG_REGEX','IP_VM_TEMP','TEAM_IP_RANGE','OUR_TEAM_ID',
                    'TICK_TIME','SEC_SECONDS','TIMEOUT_ATTACK','THREADING_LIMIT',
                    'AUTO_BLACKLIST_ON','TIMES_TO_BLACKLIST','TIME_TO_WAIT_IN_BLACKLIST'],
        'log_name':lambda: ['@global','@all','@flag'] + list_process_array(),
        }
    

    #Can modify the command excluing the code under this
    def __init__(self):
        super().__init__()
        self.__command_factory_init(self.routes.keys(),self.completeall,self.docommand)
    
    def __gen_do_fun(self,do_fun,command_name):
        return lambda self,a: do_fun(a,command_name)

    def __command_factory_init(self,command_list,hint_fun,do_fun):
        class_obj = self.__class__
        for command in command_list:
            setattr(class_obj,f'complete_{command}',hint_fun)
            fun = self.__gen_do_fun(do_fun,command)
            setattr(class_obj,f'do_{command}',fun)

    def get_full_hint(self,h_list,text):
        res = []
        for ele in h_list:
            if '::' in ele:
                name = [f for f in ele.split('::') if f != ''][-1]
                custom_type = ele.split('::')[0]
                if custom_type in self.hint_vars.keys():
                    if type(self.hint_vars[custom_type]) == list:
                        res += [f for f in self.hint_vars[custom_type] if f.startswith(text)]
                    else:
                        res += [f for f in self.hint_vars[custom_type]() if f.startswith(text)]
                else:
                    res.append(f'<{name}>')
            else:
                if ele.startswith(text):
                    res.append(ele)
        return res

    def docommand(self, line, command_name):
        params = getParamethers(line)
        hint_list = self.routes[command_name]
        c_vars = []
        while True:
            if type(hint_list) == list:
                if params:
                    c_vars += params
                if len(hint_list) == 2:
                    return hint_list[0](*hint_list[1],*c_vars)
                elif len(hint_list) == 1:
                    return hint_list[0](*c_vars)
                else:
                    print(self.uncompleted_command)
                    break
            if type(hint_list) == dict:
                if len(params) != 0:
                    to_see = params.pop(0)
                    if to_see in hint_list.keys():
                        hint_list = hint_list[to_see]
                    elif '::' in ''.join(list(hint_list.keys())):
                        selected = None
                        for ele in hint_list.keys():
                            if '::' in ele:
                                selected = ele
                                break
                        c_vars.append(to_see)
                        hint_list = hint_list[selected]
                    else:
                        print(self.uncompleted_command)
                        break
                else:
                    print(self.uncompleted_command)
                    break
            else:
                print(self.uncompleted_command)
                break
    
    def completeall(self, text, line, begidx, endidx):
        params = getParamethers(line)
        hint_list = self.routes[params.pop(0)]
        while True:
            if type(hint_list) == dict:
                go_on = False
                if text:
                    go_on = len(params) != 1
                else:
                    go_on = len(params) != 0
                if go_on:
                    to_see = params.pop(0)
                    if to_see in hint_list.keys():
                        hint_list = hint_list[to_see]
                    elif '::' in ''.join(list(hint_list.keys())):
                        selected = None
                        for ele in hint_list.keys():
                            if '::' in ele:
                                selected = ele
                                break
                        hint_list = hint_list[selected]
                    else:
                        return []
                else:
                    return self.get_full_hint(list(hint_list.keys()),text)
            else:
                return []
    
    def do_exit(self,line):
        "Exit from CTFsub command line"
        exit()

class InvalidCommand(Exception):pass

if __name__ == '__main__':
    shell = CTFsubShell()
    while True:
        try:shell.cmdloop()
        except (KeyboardInterrupt,InterruptedError):print()
        except (InvalidCommand):print('Invalid command D:')

