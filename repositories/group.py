from models import Group
from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned

from exceptions import InvalidFieldOrValueException


class GroupRepository:

    @staticmethod
    async def create_group(payload):
        group = await Group.create(name=payload.get("group_name"))
        return group

    @staticmethod
    async def add_user_to_group(group, user):
        await user.groups.add(group)

    @staticmethod
    async def get_group_by_filters(payload):
        try:
            group = await Group.get(**payload)
        except DoesNotExist as e:
            raise InvalidFieldOrValueException(
                message="No 'Group' object exists with given fields", context=payload
            )
        except ModuleNotFoundError as e:
            raise InvalidFieldOrValueException(
                message="Multiple 'Group' object exists with given fields",
                context=payload,
            )
        return group

    @staticmethod
    async def get_users_of_group(group):
        return await group.users.all()
