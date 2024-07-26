from functools import wraps
from managers import AuthManager

def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            await AuthManager.check_token(request)
            res = await f(request,*args, **kwargs)
            return res
        return decorated_function
    return decorator(wrapped)

def group_member_permission(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request,static_id,*args, **kwargs):
            await AuthManager.check_group_member(request,static_id)
            res = await f(request,static_id,*args, **kwargs)
            return res
        return decorated_function
    return decorator(wrapped)

def expense_member_permission(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request,static_id,*args, **kwargs):
            await AuthManager.check_expense_group_member(request,static_id)
            res = await f(request,static_id,*args, **kwargs)
            return res
        return decorated_function
    return decorator(wrapped)