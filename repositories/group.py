
from models import Group
class GroupRepository:
    
    
    @staticmethod
    async def create_group(payload):
        group = await Group.create(name = payload.get("group_name"))
        return group
    
    @staticmethod
    async def add_user_to_group(group,user):
        await user.groups.add(group)
        
    @staticmethod
    async def get_group_by_filters(payload):
        group = await Group.get(**payload)
        return group
    
    @staticmethod
    async def get_users_of_group(group):
        return await group.users.all()
    
        