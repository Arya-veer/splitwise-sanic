from tortoise.contrib.sanic import register_tortoise

import os,json
from configurations.settings import BASE_DIR

DB_CONFIG_PATH = os.path.join(BASE_DIR,"db","db_config.json")

with open(DB_CONFIG_PATH,"r") as f:
    TORTOISE_ORM = json.loads(f.read())

def connect_tortoise_to_db(app):
    register_tortoise(app,config_file=DB_CONFIG_PATH,generate_schemas=False)