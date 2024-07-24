from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "Group" (
    "static_id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(30) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "total_expense" DECIMAL(6,2) NOT NULL  DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "User" (
    "static_id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(30) NOT NULL,
    "password" VARCHAR(100),
    "email" VARCHAR(40) NOT NULL,
    "secret" UUID  UNIQUE
);
CREATE TABLE IF NOT EXISTS "Expense" (
    "static_id" UUID NOT NULL  PRIMARY KEY,
    "title" VARCHAR(50) NOT NULL,
    "description" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "amount" INT NOT NULL  DEFAULT 0,
    "group_id" UUID NOT NULL REFERENCES "Group" ("static_id") ON DELETE CASCADE,
    "uploaded_by_id" UUID NOT NULL REFERENCES "User" ("static_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "ExpenseUser" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "amount" INT NOT NULL,
    "has_paid" BOOL NOT NULL  DEFAULT False,
    "expense_id" UUID NOT NULL REFERENCES "Expense" ("static_id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "User" ("static_id") ON DELETE CASCADE,
    CONSTRAINT "uid_ExpenseUser_expense_1fbd5d" UNIQUE ("expense_id", "user_id")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "User_Group" (
    "User_id" UUID NOT NULL REFERENCES "User" ("static_id") ON DELETE CASCADE,
    "group_id" UUID NOT NULL REFERENCES "Group" ("static_id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_User_Group_User_id_5d1db0" ON "User_Group" ("User_id", "group_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
