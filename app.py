from sanic import Sanic
from db.register import connect_tortoise_to_db
from routes import api_blueprint_group


app = Sanic("splitwise")
connect_tortoise_to_db(app=app)
app.blueprint(api_blueprint_group)
