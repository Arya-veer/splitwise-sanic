
from serializers import ExpenseSerializer
from repositories import ExpenseRepository


class ExpenseManager:
    
    _expense = None
    
    @classmethod
    async def view_expense(cls):
        return await ExpenseSerializer.serialize_expense(cls._expense)
    
    @classmethod
    async def delete_expense(cls):
        await ExpenseRepository.delete_expense(cls._expense)