from tortoise.queryset import QuerySet
from .user import UserSerializer
from models import Expense


class ExpenseSerializer:

    @staticmethod
    async def serialize_expense_users(qs: QuerySet):
        data = []
        for obj in qs:
            user = await obj.user
            serialized_data = {
                "user": UserSerializer.serialize_user(user),
                "amount": obj.amount,
                "has_paid": obj.has_paid,
            }
            data.append(serialized_data)
        return data

    @staticmethod
    async def serialize_expenses(qs: QuerySet[Expense]):
        data = []
        for obj in qs:
            user = await obj.uploaded_by
            serialized_obj = {
                "static_id": str(obj.static_id),
                "title": obj.title,
                "description": obj.description,
                "created_by": UserSerializer.serialize_user(user),
                "created_at": obj.created_at.strftime("%d %B, %Y"),
                "amount": obj.amount,
            }
            data.append(serialized_obj)
        return data

    @staticmethod
    async def serialize_expense(expense: Expense):
        user = await expense.uploaded_by
        paid_by = await expense.expense_users.filter(has_paid=True)
        paid_for = await expense.expense_users.filter(has_paid=False)
        group = await expense.group

        return {
            "static_id": str(expense.static_id),
            "title": expense.title,
            "description": expense.description,
            "created_by": UserSerializer.serialize_user(user),
            "created_at": expense.created_at.strftime("%d %B, %Y"),
            "amount": expense.amount,
            "paid_by": await ExpenseSerializer.serialize_expense_users(paid_by),
            "paid_for": await ExpenseSerializer.serialize_expense_users(paid_for),
            "group": {"static_id": group.static_id, "name": group.name},
        }
