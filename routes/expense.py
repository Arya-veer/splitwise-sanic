from sanic import response,Blueprint

from decorators.auth import expense_member_permission

from managers import ExpenseManager

expense_blueprint = Blueprint("Expense","/expense")

@expense_blueprint.get("/<static_id:uuid>")
@expense_member_permission
async def view_expense(request,static_id,*args, **kwargs):
    expense = await ExpenseManager.view_expense()
    return response.json(expense)


@expense_blueprint.delete("/<static_id:uuid>")
@expense_member_permission
async def delete_expense(request,static_id):
    await ExpenseManager.delete_expense()
    return response.json({"message":"Expense deleted successfully"})

@expense_blueprint.patch("/<static_id:uuid>/rename")
@expense_member_permission
async def rename_expense(request,static_id):
    data = await ExpenseManager.rename_expense(request.json)
    return response.json({"message":"Title changed successfully","data":data})