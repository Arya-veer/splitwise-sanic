from sanic.handlers import ErrorHandler
from sanic import response

class CustomErrorHandler(ErrorHandler):
    def default(self, request, exception: Exception):
        status_code = getattr(exception, "status_code", 400)
        
        return response.json(
            {
                "error":str(exception)
            },
            status=status_code
        )
