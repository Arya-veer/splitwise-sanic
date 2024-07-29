from redis.asyncio import Redis

from functools import wraps


class RedisCache:

    __redis_cache = Redis(decode_responses=True)
    _prefix = ""
    _expiry = 60 * 10

    @classmethod
    def get_redis(cls):
        return cls.__redis_cache

    @staticmethod
    def prefix_key(f):
        @wraps(f)
        async def wrapper(cls, key, *args):
            if not isinstance(key, str):
                raise Exception(f"Redis key:'{key}' can only be string")
            if cls._prefix:
                key = f"splitwise:{cls._prefix}:{key}"
            else:
                key = f"splitwise:{key}"
            return await f(cls, key, *args)

        return wrapper

    @classmethod
    @prefix_key
    async def set(cls, key, val):
        if isinstance(val, dict):
            await cls.__redis_cache.hmset(key, val)
            await cls.__redis_cache.expire(key, cls._expiry)
        else:
            await cls.__redis_cache.set(key, val, cls._expiry)

    @classmethod
    @prefix_key
    async def get(cls, key):
        value = await cls.__redis_cache.get(key)
        return value

    @classmethod
    @prefix_key
    async def delete(cls, key, more_keys):
        await cls.__redis_cache.delete(key, *list(map(cls.prefix_key, more_keys)))

    @classmethod
    @prefix_key
    async def get_dict(cls, key):
        value = await cls.__redis_cache.hgetall(key)
        return value

    @classmethod
    @prefix_key
    async def sadd(cls, key, *values):
        await cls.__redis_cache.sadd(key, *values)

    @classmethod
    @prefix_key
    async def smembers(cls, key):
        members = await cls.__redis_cache.smembers(key)
        return list(members)
