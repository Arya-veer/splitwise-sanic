
from redis.asyncio import Redis

class RedisCache:
    
    __redis_cache = None
    _prefix = ""
    _expiry = 60*10
    
    @classmethod
    def prefix_key(cls,key):
        return cls._prefix + "_" + key
    
    @classmethod
    def setup(cls):
        cls.__redis_cache = Redis()
        
    @classmethod
    async def set(cls,key,val):
        if not isinstance(key,str):
            raise Exception("Redis key can only be string")
        print(val)
        if isinstance(val,dict):
            await cls.__redis_cache.hmset(cls.prefix_key(key),val)
            await cls.__redis_cache.expire(cls.prefix_key(key),cls._expiry)
        else:
            await cls.__redis_cache.set(cls.prefix_key(key),val,cls._expiry)

        
    @classmethod
    async def get(cls,key):
        if not isinstance(key,str):
            raise Exception("Redis key can only be string")
        value = await cls.__redis_cache.get(cls.prefix_key())
        return value
    
    @classmethod
    async def delete(cls,key,more_keys):
        if not isinstance(key,str):
            raise Exception("Redis key can only be string")
        
        await cls.__redis_cache.delete(cls.prefix_key(key),*list(map(cls.prefix_key,more_keys)))