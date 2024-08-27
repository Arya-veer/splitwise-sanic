from .base_split import BaseSplit
from exceptions import IncompleteParametersException,InvalidFieldOrValueException
from uuid import UUID


class ExactSplit(BaseSplit):
    
    async def validate_data(self, data):
        await super().validate_data(data)
        if "users_map" not in data:
            raise IncompleteParametersException("Field 'users_map' not present ")
        if not isinstance(data["users_map"],dict):
            raise InvalidFieldOrValueException("Field 'users_map' should be a 'dict'")
        if not all([isinstance(x,UUID) and isinstance(y,int) for x,y in data["users_map"].items()]):
            raise InvalidFieldOrValueException("Invalid user map entry")
        if not sum(data["users_map"].values()) == data["amount"]:
            raise InvalidFieldOrValueException("Sum of amount should be 100")
    
    async def split(self, data):
        users_map = data["users_map"]
        result = []
        for user,amount in users_map.items():
            result.append({
                "user_id":user,
                "amount":amount,
            })
        return result