from models import Expense, ExpenseUser

from tortoise.queryset import QuerySet

from tortoise.transactions import in_transaction


class ExpenseUserRepository:

    @staticmethod
    async def get_from_filters(
        payload: dict, ordering: str = "id"
    ) -> QuerySet[ExpenseUser]:

        expense_users = await ExpenseUser.filter(**payload).order_by(ordering)
        return expense_users

    @staticmethod
    async def create_expense_user(payload):
        expense_user = await ExpenseUser.create(**payload)


class ExpenseRepository:

    @staticmethod
    async def get_expense_by_filters(payload):
        expense = await Expense.get(**payload)
        return expense

    @staticmethod
    async def get_expenses_by_fiters(payload, ordering="title"):
        expenses = await Expense.filter(**payload).order_by(ordering)
        return expenses

    @staticmethod
    async def add_expense(group, user, payload):
        expense = await Expense.create(**payload, group=group, uploaded_by=user)
        return expense

    @staticmethod
    async def delete_expense(expense: Expense):
        await expense.delete()

    @staticmethod
    async def edit_expense(expense: Expense, payload):
        expense_updated = expense.update_from_dict(data=payload)
        expense_updated = await expense_updated.save(update_fields=list(payload.keys()))
        return expense_updated
