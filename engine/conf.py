import os

DEBUG = os.getenv("DEBUG","False").lower() in ('true','1','t')
MONGO_URL = "mongodb://mongo/"
MAX_DATA_HOOK = 1024*512 # 0.5 Mb
SOCKET_HOOK_ADDR = "0.0.0.0"
SOCKET_HOOK_PORT = 4040

ATTACKER = None
SUBMITTER = None

SETTINGS_SUBMITTER = None

