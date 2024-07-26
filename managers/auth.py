import jwt
from repositories import UserRepository,GroupRepository,ExpenseRepository
from managers import UserManager,GroupManager,ExpenseManager
from exceptions import PermissionNotGrantedException

from configurations.settings import AUTH_SECRET
   
class AuthManager:
        
    @staticmethod
    async def check_token(request):
        if not request.token:
            raise PermissionNotGrantedException()
        payload = jwt.decode(request.token, AUTH_SECRET, algorithms=["HS256"])
        users = await UserRepository.fetch_users({"static_id":payload.get("user_id")})
        if len(users) == 0:
            raise PermissionNotGrantedException()
        UserManager._user = users[0]
        
    @staticmethod
    async def check_group_member(request,static_id):
        await AuthManager.check_token(request)
        group = await GroupRepository.get_group_by_filters({"static_id":static_id})
        GroupManager._group = group
        GroupManager._group_users = await GroupRepository.get_users_of_group(group)
        if UserManager._user not in GroupManager._group_users:
            raise PermissionNotGrantedException(message="Can not access this group as you are not a member")
        
    @staticmethod
    async def check_expense_group_member(request,static_id):
        await AuthManager.check_token(request)
        expense = await ExpenseRepository.get_expense_by_filters({"static_id":static_id})
        ExpenseManager._expense = expense
        group = await expense.group
        await AuthManager.check_group_member(request,group.static_id)