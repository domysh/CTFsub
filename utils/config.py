import os, logging, utils.fun
from os.path import join as pjoin

SUB_URL = 'https://finals.cyberchallenge.it/submit'
TEAM_TOKEN = '461KEFD3kfscDZPx'

ROOT_DIR = os.path.abspath('.')

FLAG_REGEX = 'flg\\{[A-Za-z0-9]{25}\\}'

LOG_FOLDER = pjoin(ROOT_DIR,'logs')
utils.fun.create_if_not_exist( LOG_FOLDER )
ATTACK_PKG = 'attacks'
ATTACKS_FOLDER = pjoin(ROOT_DIR,ATTACK_PKG)
utils.fun.create_if_not_exist( ATTACKS_FOLDER )
utils.fun.create_file(pjoin(ATTACKS_FOLDER,'__init__.py'))

IP_VM_TEMP = "10.10.@team_id.1"

TEAM_IP_RANGE = (1,28)

OUR_TEAM_ID = 5

TICK_TIME = 1.5 * 60
SEC_SECONDS = 3

TIMEOUT_ATTACK = 40

THREADING_LIMIT = 7

TIMES_TO_BLACKLIST = 4
TIME_TO_WAIT_IN_BLACKLIST = 6


PRINT_LOGS = False

GLOBAL_DATA_FILE = pjoin(ROOT_DIR,'g_var.json')
GLOBAL_SETTINGS_FILE = pjoin(ROOT_DIR,'settings.json')

GLOBAL_LOG_FILE = pjoin(LOG_FOLDER,'CTFsub.log')
utils.fun.create_file(GLOBAL_LOG_FILE)

GLOBAL_FLAG_FILE = pjoin(LOG_FOLDER,'flags.log')
utils.fun.create_file(GLOBAL_LOG_FILE)




