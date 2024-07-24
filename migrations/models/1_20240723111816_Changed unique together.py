from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE UNIQUE INDEX "uid_ExpenseUser_expense_ab84c2" ON "ExpenseUser" ("expense_id", "user_id", "has_paid");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "uid_ExpenseUser_expense_ab84c2";
        CREATE UNIQUE INDEX "uid_ExpenseUser_expense_1fbd5d" ON "ExpenseUser" ("expense_id", "user_id");"""
