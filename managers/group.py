from validators import GroupValidator,ExpenseValidator
from repositories import GroupRepository,UserRepository,ExpenseRepository
from serializers import GroupSerializer,UserSerializer,ExpenseSerializer
from .user import UserManager

class GroupManager:
    
    _group = None
    _group_users = None
    
    @staticmethod
    async def create_group(payload):
        GroupValidator.validate_create_group(payload)
        group = await GroupRepository.create_group(payload)
        await GroupRepository.add_user_to_group(group,UserManager._user)
        serialized_group = GroupSerializer.serialize_group(group)
        return serialized_group
    
    @staticmethod
    async def list_groups_of_user():
        groups = await UserRepository.get_all_groups(UserManager._user)
        return GroupSerializer.serialize_groups(groups)
    
    @classmethod
    async def add_users(cls,payload):
        group = cls._group
        GroupValidator.validate_add_users(payload)
        users = await UserRepository.fetch_users({"email__in":payload.get("emails")})
        await group.users.add(*users)
        
    @classmethod
    def list_users(cls):
        return UserSerializer.serialize_users(cls._group_users)
    
    @classmethod
    async def add_expense(cls,payload):
        ExpenseValidator.validate_create_expense(payload,cls._group,UserManager._user)
        expense = await ExpenseRepository.add_expense(cls._group,UserManager._user,payload)
        serialized_expense = await ExpenseSerializer.serialize_expense(expense)
        return serialized_expense
    
    @classmethod
    async def list_expenses(cls):
        expenses = await ExpenseRepository.get_expenses_by_fiters({"group":cls._group})
        return await ExpenseSerializer.serialize_expenses(expenses)
    
    @classmethod
    async def delete_group(cls):
        print(cls._group)
        await cls._group.delete()
        cls._group = None