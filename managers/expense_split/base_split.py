from abc import ABC,abstractmethod
from exceptions import IncompleteParametersException,InvalidFieldOrValueException

class BaseSplit(ABC):
    
    async def validate_data(self,data:dict):
        if "has_paid" not in data:
            raise IncompleteParametersException("Field 'has_paid' not present ")
        if not isinstance(data["has_paid"],bool):
            raise InvalidFieldOrValueException("Field 'has_paid' should be a 'bool'")
        if "amount" not in data:
            raise IncompleteParametersException("Field 'amount' not present ")
        if not isinstance(data["amount"],(float,int)):
            raise InvalidFieldOrValueException("Field 'amount' should be a 'number'")
            
    
    @abstractmethod
    async def split_util(self,data):
        raise NotImplementedError()
    
    async def split(self,data):
        self.result = []
        await self.validate_data(data)
        await self.split_util(data)
        for val in self.result:
            val["has_paid"] = data["has_paid"]
        return self.result
        