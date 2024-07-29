from models import User, UserGroup


class UserRepository:

    @staticmethod
    async def get_or_create_user(payload):
        user, created = await User.get_or_create(email=payload.get("email"))
        if created:
            user.name = payload.get("name")
            user.set_password(payload.password())
            await user.save()
        return user

    @staticmethod
    async def fetch_users(payload):
        users = await User.filter(**payload)
        return users

    @staticmethod
    async def get_all_groups(user):
        groups = await user.groups.all()
        return groups


class UserGroupRepository:

    @staticmethod
    async def get_user_group(payload):
        print(payload)
        print(payload)
        user_group = await UserGroup.get(**payload)
        return user_group

    @staticmethod
    async def update_user_group_amount(user_group: UserGroup, amount=0):
        user_group.settled_amount += amount
        await user_group.save()

    @staticmethod
    async def get_user_groups(payload, ordering="id"):
        user_groups = await UserGroup.filter(**payload).order_by(ordering)
        return user_groups
