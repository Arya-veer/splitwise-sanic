from sanic import response,Blueprint

from managers import GroupManager

from decorators.auth import protected,group_member_permission


group_blueprint = Blueprint("Group","/group")

@group_blueprint.post("")
@protected
async def create_group(request):
    group = await GroupManager.create_group(request.json)
    return response.json({"message":"Group created successfully","data":group},status=201)

@group_blueprint.get("/list")
@protected
async def get_groups(request):
    groups = await GroupManager.list_groups_of_user()
    return response.json(groups,status=200)

@group_blueprint.delete("/<static_id:uuid>")
@group_member_permission
async def delete_group(request,static_id):
    await GroupManager.delete_group()
    return response.json({"message":"Group Deleted"})

@group_blueprint.post("/<static_id:uuid>/add_users")
@group_member_permission
async def add_users(request,static_id):
    print(request.json)
    await GroupManager.add_users(request.json)
    return response.json({"message":"Added users to group"},status=200)


@group_blueprint.get("/<static_id:uuid>/list_users")
@group_member_permission
async def list_users(request,static_id):
    users = GroupManager.list_users()
    return response.json(users)
    


@group_blueprint.post("/<static_id:uuid>/add_expense")
@group_member_permission
async def add_expense(request,static_id):
    expense = await GroupManager.add_expense(request.json)
    return response.json({"message":"Expense added","data":expense},status=200)


@group_blueprint.get("/<static_id:uuid>/view_expenses")
@group_member_permission
async def list_expenses(request,static_id):
    expenses = await GroupManager.list_expenses()
    return response.json(expenses)
    