from .redis import RedisCache


class CurrencyRatesCache(RedisCache):
    
    _prefix = "currency"
    
    @classmethod
    async def set_rates(cls,data):
        await cls.get_redis().hmset("rates",data["rates"])
        await cls.get_redis().expireat("rates",data["time_next_update_unix"])
        
    @classmethod
    async def get_rates(cls):
        rates_dict = await cls.get_redis().hgetall("rates")
        print(rates_dict)
        return rates_dict