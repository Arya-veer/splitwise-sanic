from sanic import Blueprint
from routes.group import group_blueprint
from routes.auth import auth_blueprint
from routes.expense import expense_blueprint




api_blueprint_group = Blueprint.group(url_prefix="/api")

def config_blueprints():
    api_blueprint_group.append(group_blueprint)
    api_blueprint_group.append(auth_blueprint)
    api_blueprint_group.append(expense_blueprint)
    
config_blueprints()