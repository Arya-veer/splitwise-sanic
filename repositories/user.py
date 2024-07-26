from models import User

class UserRepository:
    
    @staticmethod
    async def get_or_create_user(payload):
        user,created = await User.get_or_create(email=payload.get("email"))
        if created:
            user.name = payload.get("name")
            user.set_password(payload.password())
            await user.save()
        return user
    
    @staticmethod
    async def fetch_users(payload):
        print(payload)
        users = await User.filter(**payload)
        print(payload)
        return users
    
    @staticmethod
    async def get_all_groups(user):
        groups = await user.groups.all()
        return groups
    