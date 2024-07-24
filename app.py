from sanic import Sanic
from db.register import connect_tortoise_to_db
from routes import api_blueprint_group

from configurations.settings import BASE_DIR,AUTH_SECRET,PASSWORD_SECRET

app = Sanic("splitwise")
app.config.AUTH_SECRET = AUTH_SECRET
app.config.PASSWORD_SECRET = PASSWORD_SECRET
app.config.AUTH_LOGIN_ENDPOINT = 'login'
app.config.BASE_DIR = BASE_DIR
connect_tortoise_to_db(app=app)
app.blueprint(api_blueprint_group)
