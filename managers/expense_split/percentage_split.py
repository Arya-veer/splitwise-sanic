from .base_split import BaseSplit
from exceptions import IncompleteParametersException,InvalidFieldOrValueException
from uuid import UUID


class PercentageSplit(BaseSplit):
    
    async def validate_data(self, data):
        await super().validate_data(data)
        if "users_map" not in data:
            raise IncompleteParametersException("Field 'users_map' not present ")
        if not isinstance(data["users_map"],dict):
            raise InvalidFieldOrValueException("Field 'users_map' should be a 'dict'")
        if not all([isinstance(x,UUID) and isinstance(y,int) for x,y in data["users_map"].items()]):
            raise InvalidFieldOrValueException("Invalid user map entry")
        if not sum(data["users_map"].values()) == 100:
            raise InvalidFieldOrValueException("Sum of percentages should be 100")
            
    
    async def split_util(self, data):
        total = data["amount"]
        users_map = data["users_map"]
        for user,percent in users_map.items():
            self.result.append({
                "user_id":user,
                "amount":total*(percent/100),
            })
        return self.result