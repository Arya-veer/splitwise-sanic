from sanic import Sanic
from db.register import connect_tortoise_to_db
from routes import api_blueprint_group
from exceptions import CustomErrorHandler


app = Sanic("splitwise")
connect_tortoise_to_db(app=app)
app.blueprint(api_blueprint_group)
# app.error_handler = CustomErrorHandler()
