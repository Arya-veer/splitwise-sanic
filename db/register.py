from tortoise.contrib.sanic import register_tortoise

import os, json
from configurations.settings import BASE_DIR

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

with open(CONFIG_PATH, "r") as f:
    TORTOISE_ORM = json.loads(f.read())["DATABASE"]

def connect_tortoise_to_db(app):
    register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)