from .abstract_redis import RedisCache

class GroupCache(RedisCache):
    
    _prefix = "group"