
from core.exceptions import IncompleteParametersException

class UserValidator:
    
    @staticmethod
    def validate_signup_params(payload):
        if "name" not in payload or "email" not in payload or "password" not in payload:
            raise IncompleteParametersException()
        
    @staticmethod
    def validate_login_params(payload):
        if "email" not in payload or "password" not in payload:
            raise IncompleteParametersException()
        
    @staticmethod
    def validate_change_password(payload):
        if "password" not in payload:
            raise IncompleteParametersException()