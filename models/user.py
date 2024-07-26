from tortoise import fields,models,validators
import uuid
import bcrypt
from sanic import Sanic
from tortoise import exceptions

from configurations.settings import PASSWORD_SECRET

class UserGroup(models.Model):
    user = fields.ForeignKeyField("models.User","user_groups")
    group = fields.ForeignKeyField("models.Group","user_groups")
    settled_amount = fields.IntField(default = 0)
    
    class Meta:
        table = "User_Group"

class User(models.Model):

    static_id = fields.UUIDField(primary_key = True,default = uuid.uuid4, unique = True)
    name = fields.CharField(max_length=30,null=True)
    password = fields.CharField(max_length=100,null=True)
    email = fields.CharField(max_length=40,validators=[validators.RegexValidator(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',0)])
    groups = fields.ManyToManyField("models.Group",related_name="users",through="UserGroup")
    secret = fields.UUIDField(unique = True,null = True)
    
    class Meta:
        table = "User"
    
    def __str__(self) -> str:
        return f"{self.name} - {self.email}"
    
    def set_password(self,password):
        if self.secret is None:
            self.secret = uuid.uuid4()
        master_secret_key = PASSWORD_SECRET
        combined_password = password + master_secret_key + str(self.secret)
        self.password = bcrypt.hashpw(combined_password,bcrypt.gensalt())
    
    @classmethod
    async def authenticate(cls,email,password):
        try:
            user = await User.get(email=email)
        except exceptions.DoesNotExist:
            return None
        app = Sanic.get_app("splitwise")
        master_secret_key = PASSWORD_SECRET
        combined_password = password + master_secret_key + str(user.secret)
        if bcrypt.checkpw(combined_password,user.password):
            return user
        return None
    
    
    
    