#Inset here the regex for the flag for a better selection, else insert None
FLAG_REGEX = 'flg\\{[A-Za-z0-9]{25}\\}'

#here you can create you template ip for generate address go other teams
#@Team_id will be substituded with a number in TEAM_IP_RANGE
IP_VM_TEMP = "10.10.@team_id.1"

TEAM_IP_RANGE = (1,28)
#Set here your team id for skip the attack
OUR_TEAM_ID = 5
#Set how much time wait from a round to another
TICK_TIME = 1.5 * 60
#Final seconds to wait with a segnalation on Global log
SEC_SECONDS = 3

#Max time for an attack (If not specified on attack config)
TIMEOUT_ATTACK = 40

#Set how many thread activate for the attack
THREADING_LIMIT = 7

#Manage Autoblacklist settings
AUTO_BLACKLIST_ON = True
TIMES_TO_BLACKLIST = 4
TIME_TO_WAIT_IN_BLACKLIST = 6

#If this is true and you start the program from start.py you can see all the logs in stdout
PRINT_LOGS = False

#This function will be used for submit recived flags so you can adapt this for your A/D gameserver
def flag_submit(flag):
    import requests
    requests.post('https://finals.cyberchallenge.it/submit',
        data={'team_token': '461KEFD3kfscDZPx', 'flag': flag},timeout=3)

#Config for folders and other... Changing these settings can be dangerous!

import os, utils.fun
from os.path import join as pjoin

ROOT_DIR = os.path.abspath('.')
LOG_FOLDER = pjoin(ROOT_DIR,'logs')
utils.fun.create_if_not_exist( LOG_FOLDER )
ATTACK_PKG = 'attacks'
ATTACKS_FOLDER = pjoin(ROOT_DIR,ATTACK_PKG)
utils.fun.create_if_not_exist( ATTACKS_FOLDER )
utils.fun.create_file(pjoin(ATTACKS_FOLDER,'__init__.py'))

GLOBAL_DATA_FILE = pjoin(ROOT_DIR,'g_var.json')
GLOBAL_SETTINGS_FILE = pjoin(ROOT_DIR,'settings.json')

GLOBAL_LOG_FILE = pjoin(LOG_FOLDER,'CTFsub.log')
utils.fun.create_file(GLOBAL_LOG_FILE)

GLOBAL_FLAG_FILE = pjoin(LOG_FOLDER,'flags.log')
utils.fun.create_file(GLOBAL_LOG_FILE)

SHELL_CAN_USE = ['FLAG_REGEX','TICK_TIME','SEC_SECONDS',
                'TIMEOUT_ATTACK','THREADING_LIMIT','AUTO_BLACKLIST_ON',
                'TIMES_TO_BLACKLIST','TIME_TO_WAIT_IN_BLACKLIST']
