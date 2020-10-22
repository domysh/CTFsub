from config import *

#If this is true and you start the program from start.py you can see all the logs in stdout
PRINT_LOGS = False

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

GLOBAL_DATA_FILE = pjoin(LOG_FOLDER,'g_var.json')
GLOBAL_SETTINGS_FILE = pjoin(LOG_FOLDER,'settings.json')

GLOBAL_LOG_FILE = pjoin(LOG_FOLDER,'CTFsub.log')
utils.fun.create_file(GLOBAL_LOG_FILE)

GLOBAL_FLAG_FILE = pjoin(LOG_FOLDER,'flags.log')
utils.fun.create_file(GLOBAL_LOG_FILE)

SHELL_CAN_USE = ['FLAG_REGEX','TICK_TIME','SEC_SECONDS',
                'TIMEOUT_ATTACK','THREADING_LIMIT','AUTO_BLACKLIST_ON',
                'TIMES_TO_BLACKLIST','TIME_TO_WAIT_IN_BLACKLIST']
