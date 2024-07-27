from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "User_Group" RENAME TO "UserGroup";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "UserGroup" RENAME TO "User_Group";"""
