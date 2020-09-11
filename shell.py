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
    return [f for f in line.split(' ') if f != '']

def list_process_array():
    return [f for f in utils.fun.get_pythonfile_list(utils.config.ATTACKS_FOLDER) if f != '__init__']

def print_div():print('-'*30)

def list_process():
    print_div()
    for proc_key in glob.settings['process_controller'].keys():
        proc = glob.settings['process_controller'][proc_key]
        print(f'Name: {proc_key} - status: {bool_onoff(proc["on"])}')
    print_div()

def bool_onoff(v:bool):
    if v: return 'on'
    else: return 'off'

def get_set_gvar(attack_name,ip,key,value = None):
    if value is None:
        try:
            val_to_print = glob.g_var[attack_name][ip][key]
            print(f'Gvar on {attack_name}:{ip} [\'{key}\'] = {val_to_print}')
        except Exception as e:
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
                        'set':{'ip_array::list_all_ip':[print]},
                        'get':[print]
                    },
                    'blacklist':{
                        'set':{'ip_array::list_all_ip':[print]},
                        'get':[print]
                    },
                    'disable':[print],
                    'status':[print]

                },
                'status':[print],
                'timeout':{
                    'disable':[print],
                    'set':{
                        'num::time_in_seconds':[print]
                        }, 
                    'status':[print]
                },
                'autoblacklist':{
                    'set':{
                        'onoff::on_or_off':[print]
                    }, 
                    'status':[print] 
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
             
    complete_process = complete_config = \
    complete_log = complete_attack = completeall

    def do_process(self,a): return self.docommand(a,'process')
    def do_config(self,a): return self.docommand(a,'config')
    def do_log(self,a): return self.docommand(a,'log')
    def do_attack(self,a): return self.docommand(a,'attack')

    def do_exit(self,line):
        "Exit from CTFsub command line"
        exit()

if __name__ == '__main__':
    shell = CTFsubShell()
    while True:
        try:shell.cmdloop()
        except (KeyboardInterrupt,InterruptedError):print()



