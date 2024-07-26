from sanic.handlers import ErrorHandler
from sanic import response
from sanic.exceptions import SanicException

from tortoise.exceptions import BaseORMException


def handle_server_exceptions(request,exception:Exception):
    return response.json({
        "message":"Something went wrong",
        "error_message":str(exception)
    },status=500)
    
def handle_sanic_exceptions(request,exception:SanicException):
    status_code = getattr(exception,"status_code",500)
    error_dict = {
        "message":exception.message,   
        "context":{}
    }
    if exception.context:
        for key in exception.context:
            error_dict["context"][key] = str(exception.context[key])
    return response.json(error_dict,status=status_code)
    
    
def handle_tortoise_exceptions(request,exception:BaseORMException):
    status_code = 500
    return response.json({
        "message":str(exception),
    },status=status_code)
    

class CustomErrorHandler(ErrorHandler):
    
    pass

error_handler = CustomErrorHandler()
error_handler.add(Exception,handle_server_exceptions)
error_handler.add(SanicException,handle_sanic_exceptions)
error_handler.add(BaseORMException,handle_tortoise_exceptions)