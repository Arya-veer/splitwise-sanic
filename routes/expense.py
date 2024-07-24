from sanic import response,Blueprint
from core.auth import expense_member_permission
from serializers.expense import serialize_expense

expense_blueprint = Blueprint("Expense","/expense")



@expense_blueprint.get("/<static_id:uuid>")
@expense_member_permission
async def view_expense(request,static_id,*args, **kwargs):
    expense = kwargs.get("expense")
    return response.json(await serialize_expense(expense),status=200)