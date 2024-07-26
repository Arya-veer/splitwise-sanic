from validators import GroupValidator,ExpenseValidator
from repositories import GroupRepository,UserRepository,ExpenseRepository,ExpenseUserRepository,UserGroupRepository
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
        serialized_expenses = await ExpenseSerializer.serialize_expense(expense)
        for paid_by_user in serialized_expenses.get("paid_by"):
            user_group = UserGroupRepository.get_user_group({"user_id":paid_by_user["user"]["static_id"],"group_id":cls._group.static_id})
            await UserGroupRepository.update_user_group_amount(user_group,paid_by_user["amount"])
        for paid_for_user in serialized_expenses.get("paid_for"):
            user_group = UserGroupRepository.get_user_group({"user_id":paid_for_user["user"]["static_id"],"group_id":cls._group.static_id})
            await UserGroupRepository.update_user_group_amount(user_group,paid_for_user["amount"]*-1)
        return serialized_expenses
    
    @classmethod
    async def list_expenses(cls):
        expenses = await ExpenseRepository.get_expenses_by_fiters({"group":cls._group})
        return await ExpenseSerializer.serialize_expenses(expenses)
    
    @classmethod
    async def delete_group(cls):
        await cls._group.delete()
        cls._group = None
        
        
    @classmethod
    async def settle_up(cls,persist=False):
        user_groups_pos = await UserGroupRepository.get_user_groups({"group":cls._group,"settled_amount__gt":0},ordering="-settled_amount")
        user_groups_neg = await UserGroupRepository.get_user_groups({"group":cls._group,"settled_amount__lt":0},ordering="settled_amount")
        pos_ind = neg_ind = 0
        payments = []
        while pos_ind < len(user_groups_pos) and neg_ind < len(user_groups_neg):
            pos_user = await user_groups_pos[pos_ind].user
            neg_user = await user_groups_neg[neg_ind].user
            pos_amount = user_groups_pos[pos_ind].settled_amount
            neg_amount = user_groups_neg[neg_ind].settled_amount*-1
            if pos_amount > neg_amount:
                payments.append(
                    f"{neg_user} will pay {pos_user} Rs. {neg_amount}"
                )
                neg_ind+=1
                user_groups_pos[pos_ind].settled_amount -= neg_amount
                
            elif pos_amount < neg_amount:
                payments.append(
                    f"{neg_user} will pay {pos_user} Rs. {pos_amount}"
                )
                pos_ind+=1
                user_groups_neg[neg_ind].settled_amount += pos_amount
                
            else:
                payments.append(
                    f"{neg_user} will pay {pos_user} Rs. {neg_amount}"
                )
                pos_ind+=1
                neg_ind-=1
        return payments