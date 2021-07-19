import os

DEBUG = os.getenv("DEBUG","False").lower() in ('true','1','t')
APP_STATUS = None
MONGO_URL = "mongodb://mongo/"