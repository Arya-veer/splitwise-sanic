from tortoise import fields, models, timezone, validators
import uuid


class Group(models.Model):

    static_id = fields.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = fields.CharField(max_length=30)
    created_at = fields.DatetimeField(default=timezone.now)
    updated_at = fields.DatetimeField(auto_now=True)
    total_expense = fields.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    class Meta:
        table = "Group"

    def __str__(self) -> str:
        return f"Group {self.name}"
