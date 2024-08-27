from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "Group" DROP COLUMN "currency";
        ALTER TABLE "Expense" DROP COLUMN "currency";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "Group" ADD "currency" VARCHAR(10) NOT NULL  DEFAULT 'USD';
        ALTER TABLE "Expense" ADD "currency" VARCHAR(10) NOT NULL  DEFAULT 'USD';"""
