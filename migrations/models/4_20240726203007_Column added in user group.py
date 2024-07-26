from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "User" ALTER COLUMN "name" DROP NOT NULL;
        ALTER TABLE "User_Group" ADD "settled_amount" INT NOT NULL DEFAULT 0;
"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "User" ALTER COLUMN "name" SET NOT NULL;
        DROP TABLE IF EXISTS "User_Group";"""
