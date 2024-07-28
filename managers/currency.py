

from utils.currency import CurrencyAPIClient

from caches import CurrencyRatesCache


class CurrencyManager:
    
    @staticmethod
    async def get_all_currencies():
        rates = await CurrencyRatesCache.get_rates()
        if not rates:
            data = await CurrencyAPIClient.get()
            await CurrencyRatesCache.set_rates(data)
            rates = data["rates"]
        return rates