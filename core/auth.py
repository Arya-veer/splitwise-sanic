from functools import wraps
import jwt
from sanic import response
from models.user import User
from models.group import Group
from models.expense import Expense
from datetime import datetime

def get_token(request,user):
    token = jwt.encode({"user_id":str(user.static_id),"timestamp":str(datetime.now())},key=request.app.config.AUTH_SECRET)
    return token

async def check_token(request):
    print(request.token)
    if not request.token:
        return False,None
    try:
        payload = jwt.decode(
            request.token, request.app.config.AUTH_SECRET, algorithms=["HS256"]
        )
        
        user = await User.get(static_id = payload.get("user_id"))
    except jwt.exceptions.InvalidTokenError as e:
        print(str(e))
        return False,None
    else:
        return True,user
    

def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            print("In decorator")
            is_authenticated,user = await check_token(request)
            request.ctx.user = user
            if is_authenticated:
                res = await f(request,user = user,*args, **kwargs)
                return res
            else:
                return response.json({"message":"You are unauthorized."},status=401)
        return decorated_function
    return decorator(wrapped)


def group_member_permission(wrapped):
    def decorator(f):
        @wraps(f)
        @protected
        async def decorated_function(request,static_id,*args, **kwargs):
            group = await Group.get_or_none(static_id = static_id)
            if group is None:
                return response.json({"message":"Group does not exist"},status=400)
            current_user = kwargs.get("user")
            group_users = await group.users.all()
            if current_user not in group_users:
                return response.json({"message":"Unauthorised to access group"},status=401)
            kwargs["group"] = group
            kwargs["group_users"] = group_users
            res = await f(request,static_id,*args, **kwargs)
            return res
        return decorated_function
    return decorator(wrapped)


def expense_member_permission(wrapped):
    def decorator(f):
        @wraps(f)
        @protected
        async def decorated_function(request,static_id,*args, **kwargs):
            expense = await Expense.get_or_none(static_id = static_id)
            if expense is None:
                return response.json({"message":"Expense does not exist"},status=400)
            current_user = kwargs.get("user")
            group = await expense.group
            group_users = await group.users.all()
            if current_user not in group_users:
                return response.json({"message":"Unauthorised to access group"},status=401)
            kwargs["expense"] = expense
            res = await f(request,static_id,*args, **kwargs)
            return res
        return decorated_function
    return decorator(wrapped)