
from serializers import ExpenseSerializer
from validators import ExpenseValidator
from repositories import ExpenseRepository
from tortoise.transactions import in_transaction
from caches import ExpenseSettleCache
class ExpenseManager:
    
    _expense = None
    
    @classmethod
    async def view_expense(cls):
        return await ExpenseSerializer.serialize_expense(cls._expense)
    
    @classmethod
    async def delete_expense(cls):
        async with in_transaction():
            await ExpenseSettleCache.delete_settlements(cls._expense.group_id)
            await ExpenseRepository.delete_expense(cls._expense)
            
    @classmethod
    async def rename_expense(cls,payload):
        ExpenseValidator.validate_rename_expense(payload)
        updated_expense = await ExpenseRepository.edit_expense(cls._expense,{"title":payload.get("title")})
        serialized_updated_expense = await ExpenseSerializer.serialize_expense(updated_expense)
        return serialized_updated_expense