

from sanic import response,Blueprint

from managers import GroupManager
from tortoise import transactions

from decorators.auth import protected,group_member_permission


group_blueprint = Blueprint("Group","/group")

@group_blueprint.post("/create")
@protected
async def create_group(request,*args, **kwargs):
    group = await GroupManager.create_group(request.json)
    return response.json({"message":"Group created successfully","data":group},status=201)

@group_blueprint.get("/list")
@protected
async def get_groups(request,*args, **kwargs):
    groups = await GroupManager.list_groups_of_user()
    return response.json(groups,status=200)


@group_blueprint.post("/<static_id:uuid>/add_users")
@group_member_permission
async def add_users(request,static_id,*args, **kwargs):
    await GroupManager.add_users(request.json,kwargs.get("group"))
    return response.json({"message":"Added users to group"},status=200)


@group_blueprint.get("/<static_id:uuid>/list_users")
@group_member_permission
async def list_users(request,static_id,*args, **kwargs):
    users = GroupManager.list_users()
    return response.json(users)
    


@group_blueprint.post("/<static_id:uuid>/add_expense")
@group_member_permission
async def add_expense(request,static_id,*args, **kwargs):

    expense = await GroupManager.add_expense(request.json)
    return response.json({"message":"Expense added","data":expense},status=200)


@group_blueprint.get("/<static_id:uuid>/view_expenses")
@group_member_permission
async def list_expenses(request,static_id,*args, **kwargs):
    expenses = await GroupManager.list_expenses()
    return response.json(expenses)
    