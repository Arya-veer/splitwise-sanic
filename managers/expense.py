
from serializers import ExpenseSerializer

class ExpenseManager:
    
    _expense = None
    
    @classmethod
    async def view_expense(cls):
        return await ExpenseSerializer.serialize_expense(cls._expense)