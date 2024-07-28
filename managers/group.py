from uuid import UUID

from validators import GroupValidator,ExpenseValidator
from repositories import GroupRepository,UserRepository,ExpenseRepository,ExpenseUserRepository,UserGroupRepository
from serializers import GroupSerializer,UserSerializer,ExpenseSerializer
from caches import ExpenseSettleCache

from .user import UserManager

from tortoise.transactions import in_transaction,atomic

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
        async with in_transaction():
            users = payload.pop("users")
            expense = await ExpenseRepository.add_expense(cls._group,UserManager._user,payload)
            for user in users:
                user["expense_id"] = str(expense.static_id)
                await ExpenseUserRepository.create_expense_user(payload=user)
                user_obj = await UserRepository.fetch_users({"static_id":user["user_id"]})
                user_group = await UserGroupRepository.get_user_group({"user":user_obj[0],"group":cls._group})
                if not user['has_paid']:
                    user["amount"] *= -1
                await UserGroupRepository.update_user_group_amount(user_group,user["amount"])
            serialized_expense = await ExpenseSerializer.serialize_expense(expense)
            await ExpenseSettleCache.delete_settlements(cls._group.static_id)
            return serialized_expense
        
    
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
        settlements = await ExpenseSettleCache.get_settlements(cls._group.static_id)
        print(settlements)
        if len(settlements) > 0:
            return settlements
        user_groups_pos = await UserGroupRepository.get_user_groups({"group":cls._group,"settled_amount__gt":0},ordering="-settled_amount")
        user_groups_neg = await UserGroupRepository.get_user_groups({"group":cls._group,"settled_amount__lt":0},ordering="settled_amount")
        pos_ind = neg_ind = 0
        settlements = []
        while pos_ind < len(user_groups_pos) and neg_ind < len(user_groups_neg):
            pos_user = await user_groups_pos[pos_ind].user
            neg_user = await user_groups_neg[neg_ind].user
            pos_amount = user_groups_pos[pos_ind].settled_amount
            neg_amount = user_groups_neg[neg_ind].settled_amount*-1
            if pos_amount > neg_amount:
                settlements.append(
                    f"{neg_user} will pay {pos_user} Rs. {neg_amount}"
                )
                neg_ind+=1
                user_groups_pos[pos_ind].settled_amount -= neg_amount
                
            elif pos_amount < neg_amount:
                settlements.append(
                    f"{neg_user} will pay {pos_user} Rs. {pos_amount}"
                )
                pos_ind+=1
                user_groups_neg[neg_ind].settled_amount += pos_amount
                
            else:
                settlements.append(
                    f"{neg_user} will pay {pos_user} Rs. {neg_amount}"
                )
                pos_ind+=1
                neg_ind-=1
        # print(settlements)
        await ExpenseSettleCache.set_settlements(cls._group.static_id,settlements)
        return settlements