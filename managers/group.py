from uuid import UUID

from validators import GroupValidator, ExpenseValidator
from repositories import (
    GroupRepository,
    UserRepository,
    ExpenseRepository,
    ExpenseUserRepository,
    UserGroupRepository,
)
from serializers import GroupSerializer, UserSerializer, ExpenseSerializer
from caches import ExpenseSettleCache
from .user import UserManager
from models import Group
from models import User
from tortoise.transactions import in_transaction
from typing import List

from managers.expense_split import split_type,BaseSplit

class GroupManager:

    _group: Group = None
    _group_users: List[User] = None
    

    
    @staticmethod
    async def create_group(payload):
        
        GroupValidator.validate_create_group(payload)
        group = await GroupRepository.create_group(payload)
        await GroupRepository.add_user_to_group(group, UserManager._user)
        serialized_group = GroupSerializer.serialize_group(group)
        return serialized_group

    @staticmethod
    async def list_groups_of_user():
        groups = await UserRepository.get_all_groups(UserManager._user)
        return GroupSerializer.serialize_groups(groups)

    @classmethod
    async def add_users(cls, payload):
        group = cls._group
        GroupValidator.validate_add_users(payload)
        users = await UserRepository.fetch_users({"email__in": payload.get("emails")})
        await group.users.add(*users)

    @classmethod
    def list_users(cls):
        return UserSerializer.serialize_users(cls._group_users)
        

    @classmethod
    async def add_expense(cls, payload: dict):
        ExpenseValidator.validate_create_expense(payload, cls._group, UserManager._user)
        async with in_transaction():
            SplitManager:BaseSplit = split_type[payload.pop("split_type")]
            expense = await ExpenseRepository.add_expense(
                cls._group, UserManager._user, payload
            )
            split_manager = SplitManager()
            result = split_manager.split()
            cls._group.total_expense += expense.amount
            await cls._group.save()
            
            await ExpenseSettleCache.delete_settlements(cls._group.static_id)

    @classmethod
    async def list_expenses(cls):
        expenses = await ExpenseRepository.get_expenses_by_fiters({"group": cls._group})
        return await ExpenseSerializer.serialize_expenses(expenses)

    @classmethod
    async def delete_group(cls):
        await cls._group.delete()
        cls._group = None

    @classmethod
    async def settle_up(cls, params):
        persist = params.get("persist", False)
        settlements = await ExpenseSettleCache.get_settlements(cls._group.static_id)
        if len(settlements) > 0:
            return settlements
        user_groups_pos = await UserGroupRepository.get_user_groups(
            {"group": cls._group, "settled_amount__gt": 0}, ordering="-settled_amount"
        )
        user_groups_neg = await UserGroupRepository.get_user_groups(
            {"group": cls._group, "settled_amount__lt": 0}, ordering="settled_amount"
        )
        pos_ind = neg_ind = 0
        settlements = []
        while pos_ind < len(user_groups_pos) and neg_ind < len(user_groups_neg):
            pos_user = await user_groups_pos[pos_ind].user
            neg_user = await user_groups_neg[neg_ind].user
            pos_amount = user_groups_pos[pos_ind].settled_amount
            neg_amount = user_groups_neg[neg_ind].settled_amount * -1
                
            if pos_amount > neg_amount:
                settlements.append(
                    f"{neg_user} will pay {pos_user} Rs. {neg_amount}"
                )
                neg_ind += 1
                user_groups_pos[pos_ind].settled_amount -= neg_amount

            elif pos_amount < neg_amount:
                settlements.append(
                    f"{neg_user} will pay {pos_user} Rs. {pos_amount}"
                )
                pos_ind += 1
                user_groups_neg[neg_ind].settled_amount += pos_amount

            else:
                settlements.append(
                    f"{neg_user} will pay {pos_user} Rs. {neg_amount}"
                )
                pos_ind += 1
                neg_ind -= 1

        await ExpenseSettleCache.set_settlements(cls._group.static_id, settlements)
        return settlements
