from managers import CurrencyManager

from sanic import Blueprint
from sanic import response

currency_blueprint = Blueprint("Currency","/currencies")



@currency_blueprint.get("")
async def get_all_currencies(request,*args, **kwargs):
    rates = await CurrencyManager.get_all_currencies()
    return response.json({"message":"Available currencies","data" : list(rates.keys())})