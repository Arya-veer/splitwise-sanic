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

    @staticmethod
    async def convert_amount_to_usd(currency, amount):
        rates = await CurrencyManager.get_all_currencies()
        return rates[currency] * amount

    @staticmethod
    async def convert_amount_from_usd(currency, amount):
        rates = await CurrencyManager.get_all_currencies()
        return amount / rates[currency]

    @staticmethod
    async def convert_currency(from_currency, to_currency, amount):
        if from_currency == to_currency:
            return amount
        usd_amount = await CurrencyManager.convert_amount_to_usd(from_currency, amount)
        final_amount = await CurrencyManager.convert_amount_from_usd(
            to_currency, usd_amount
        )
        return final_amount
