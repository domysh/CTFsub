import os

DEBUG = os.getenv("DEBUG","False").lower() in ('true','1','t')
APP_STATUS = None
MONGO_URL = "mongodb://mongo/"

ENGINE_ADDR = "engine"
ENGINE_PORT = 4040


SKIO = None