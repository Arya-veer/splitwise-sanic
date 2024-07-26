
from models import Expense,ExpenseUser

from tortoise.queryset import QuerySet

from tortoise.transactions import in_transaction

class ExpenseUserRepository:
    
    @staticmethod
    async def get_from_filters(payload:dict,ordering:str = "id")->QuerySet[ExpenseUser]:
        
        expense_users = await ExpenseUser.filter(**payload).order_by(ordering)
        return expense_users
    
    

class ExpenseRepository:
    
    @staticmethod
    async def get_expense_by_filters(payload):
        expense = await Expense.get(**payload)
        return expense
    
    @staticmethod
    async def get_expenses_by_fiters(payload):
        expenses = await Expense.filter(**payload)
        return expenses 
    
    @staticmethod
    async def add_expense(group,user,payload):
        users = payload.pop("users")
        async with in_transaction():
            expense = await Expense.create(**payload,group=group,uploaded_by=user)
            for user in users:
                await ExpenseUser.get_or_create(**user,expense=expense)
        return expense
        
    @staticmethod
    async def delete_expense(expense):
        await expense.delete()