from typing import Coroutine,Any
from tortoise import fields,models
import uuid

class Expense(models.Model):
    
    static_id = fields.UUIDField(primary_key = True,default = uuid.uuid4, unique = True)
    title = fields.CharField(max_length=50)
    description = fields.TextField(default="")
    group = fields.ForeignKeyField("models.Group",related_name="expenses")
    uploaded_by = fields.ForeignKeyField("models.User",related_name="created_expenses")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    involved_users = fields.ManyToManyField("models.User",through="ExpenseUser",related_name="expenses")
    amount = fields.IntField(default = 0)
    
    class Meta:
        table = "Expense"
    
    def __str__(self) -> str:
        return f"Expense {self.title}"


class ExpenseUser(models.Model):
    expense = fields.ForeignKeyField("models.Expense","expense_users")
    user = fields.ForeignKeyField("models.User","expense_users")
    amount = fields.IntField()
    has_paid = fields.BooleanField(default=False)
    
    class Meta:
        table = "ExpenseUser"
        unique_together = [("expense","user","has_paid")]
        
    def __str__(self) -> str:
        return f"Expense: {self.expense.title}, User: {self.user.title}, Paid: {self.paid}"
    
    def save(self, using_db: models.BaseDBAsyncClient | None = None, update_fields: models.Iterable[str] | None = None, force_create: bool = False, force_update: bool = False) -> Coroutine[Any, Any, None]:
        return super().save(using_db, update_fields, force_create, force_update)