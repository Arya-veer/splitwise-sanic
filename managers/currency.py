from utils.currency import CurrencyUtil

class CurrencyManager:
    
    @staticmethod
    async def get_currencies():
        currencies = await CurrencyUtil.get_all_currencies()
        return list(currencies.keys())