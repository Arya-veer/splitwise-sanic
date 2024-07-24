from typing import List
from tortoise.queryset import QuerySet
from serializers.user import serialize_user,serialize_users

async def serialize_expense_users(qs:QuerySet):
    data = []
    for obj in qs:
        user = await obj.user
        serialized_data = {
            "user":await serialize_user(user),
            "amount":obj.amount,
            "has_paid":obj.has_paid
        }
        data.append(serialized_data)
    return data


async def serialize_expenses(qs:QuerySet):
    data = []
    for obj in qs:
        user = await obj.uploaded_by
        serialized_obj = {
            "static_id" : str(obj.static_id),
            "title": obj.title,
            "description" : obj.description,
            "created_by": await serialize_user(user),
            "created_at": obj.created_at.strftime("%d %B, %Y"),
            "amount": obj.amount
        }
        data.append(serialized_obj) 
    return data  


async def serialize_expense(expense):
    user = await expense.uploaded_by
    paid_by = await expense.expense_users.filter(has_paid = True)
    paid_for = await expense.expense_users.filter(has_paid = False)
    
    return {
        "static_id" : str(expense.static_id),
        "title": expense.title,
        "description" : expense.description,
        "created_by": await serialize_user(user),
        "created_at": expense.created_at.strftime("%d %B, %Y"),
        "amount": expense.amount,
        "paid_by": await serialize_expense_users(paid_by),
        "paid_for": await serialize_expense_users(paid_for),
    }