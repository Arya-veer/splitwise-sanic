from .base_split import BaseSplit
from exceptions import IncompleteParametersException,InvalidFieldOrValueException
from uuid import UUID

class EqualSplit(BaseSplit):
    
    async def validate_data(self, data):
        await super().validate_data(data)
        if "users" not in data:
            raise IncompleteParametersException("Field 'users' not present")
        if not isinstance(data["users"],list):
            raise InvalidFieldOrValueException("Field 'users' should be a 'list'")
        if not all((isinstance(user,UUID) for user in data["users"])):
            raise InvalidFieldOrValueException("Each entity of 'users' should be a 'uuid'")
    
    async def split_util(self, data):
        total = data["amount"]
        users = data["users"]
        count = len(users)
        for user in users:
            self.result.append({
                "user_id":user,
                "amount":total/count,
            })
        return self.result