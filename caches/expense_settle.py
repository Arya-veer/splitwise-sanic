from .redis import RedisCache



class ExpenseSettleCache(RedisCache):
    
    _prefix = "settlements"
    
    @classmethod
    async def set_settlements(cls,group_static_id,settlements):
        await cls.sadd(group_static_id,*settlements)
        
    @classmethod
    async def get_settlements(cls,group_static_id):
        settlements = await cls.smembers(group_static_id)
        return settlements
    
    @classmethod
    async def delete_settlements(cls,group_static_id):
        await cls.delete(group_static_id)