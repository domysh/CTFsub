from config import *
import utils.fun

if type(FLAG_REGEX) == bytes:
    FLAG_REGEX = FLAG_REGEX.decode()

TEAMS_LIST = []

try:
    if not USE_IP_TEMPLATE:
        TEAMS_LIST = TEAMS_IPS
    else:
        for team_id in range(TEAM_IP_RANGE[0],TEAM_IP_RANGE[1]+1):
            if team_id == OUR_TEAM_ID: continue
            TEAMS_LIST.append(utils.fun.get_ip_from_temp(IP_VM_TEMP, {'team_id':team_id})) 
except:
    exit("Error configuring teams!")

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

DB_NAME = pjoin(LOG_FOLDER,'flags.db')

INIT_DB_COMMANDS = [
"""
CREATE TABLE IF NOT EXISTS flags (
    id_flag INTEGER PRIMARY KEY,
    flag TEXT NOT NULL
)
"""
]

GLOBAL_DATA_FILE = pjoin(LOG_FOLDER,'g_var.json')
GLOBAL_SETTINGS_FILE = pjoin(LOG_FOLDER,'settings.json')

GLOBAL_LOG_FILE = pjoin(LOG_FOLDER,'CTFsub.log')
utils.fun.create_file(GLOBAL_LOG_FILE)

GLOBAL_FLAG_FILE = pjoin(LOG_FOLDER,'flags.log')
utils.fun.create_file(GLOBAL_LOG_FILE)

SHELL_CAN_USE = ['FLAG_REGEX','TICK_TIME','TIMEOUT_ATTACK',
                'THREADING_LIMIT','AUTO_BLACKLIST_ON',
                'TIMES_TO_BLACKLIST','TIME_TO_WAIT_IN_BLACKLIST']


