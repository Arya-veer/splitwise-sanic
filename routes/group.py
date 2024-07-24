
from sanic.request import Request
from sanic import response,Blueprint
from core.auth import protected,group_member_permission
from models import *
from serializers.group import serialize_groups
from serializers.user import serialize_users
from serializers.expense import serialize_expenses
from tortoise import transactions

# from serializers.group import get_serialized

group_blueprint = Blueprint("Group","/group")

@group_blueprint.post("/create")
@protected
async def create_group(request,*args, **kwargs):
    user = kwargs.get("user")
    group_name = request.json.get("group_name",None)
    group = await Group.create(name = group_name)
    await user.groups.add(group)
    return response.json({"message":"Group created successfully"},status=201)

@group_blueprint.get("/list")
@protected
async def get_groups(request,*args, **kwargs):
    user = kwargs.get("user")
    groups = await user.groups.all()
    serializer = await serialize_groups(groups)
    return response.json(serializer,status=200)


@group_blueprint.post("/<static_id:uuid>/add_users")
@group_member_permission
async def add_users(request,static_id,*args, **kwargs):
    group = kwargs.get("group")
    emails = request.json.get("emails")
    not_added_emails = []
    for email in emails:
        try:
            user = await User.get(email=email)
            await group.users.add(user)
        except User.DoesNotExist as e:
            not_added_emails.append({"email":email,"error":str(e)})
    return response.json({"message":"Added users to group","not_added_emails":not_added_emails},status=200)


@group_blueprint.get("/<static_id:uuid>/list_users")
@group_member_permission
async def list_users(request,static_id,*args, **kwargs):
    group_users = kwargs.get("group_users")
    return response.json(await serialize_users(group_users),status=200)


@group_blueprint.post("/<static_id:uuid>/add_expense")
@group_member_permission
async def add_expense(request,static_id,*args, **kwargs):
    group = kwargs.get("group")
    uploaded_by = kwargs.get("user")
    users = request.json.pop("users")
    try:
        async with transactions.in_transaction():
            expense = await Expense.create(**request.json,group=group,uploaded_by=uploaded_by)
            for user in users:
                await ExpenseUser.get_or_create(**user,expense=expense)
    except Exception as e:
        return response.json({"message":str(e)},status=400)
    return response.json({"message":"Expense added"},status=200)


@group_blueprint.get("/<static_id:uuid>/view_expenses")
@group_member_permission
async def list_expenses(request,static_id,*args, **kwargs):
    group = kwargs.get("group")
    group_expenses = await group.expenses.all()
    return response.json(await serialize_expenses(group_expenses),status=200)
    