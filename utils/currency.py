from aiohttp import ClientSession


class CurrencyAPIClient:

    _API_HOST = "https://open.er-api.com/v6/latest/USD"

    @classmethod
    async def get(cls):

        async with ClientSession() as session:
            async with session.get(cls._API_HOST) as response:
                data = await response.json()
        return data
