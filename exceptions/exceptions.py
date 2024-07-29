from sanic.exceptions import SanicException, Forbidden


class UserAlreadyExistsException(SanicException):
    message = "User Already Exists"


class IncompleteParametersException(SanicException):
    message = "All params not provided"


class PermissionNotGrantedException(Forbidden):
    message = "Unauthorized access"
    quiet = False


class InvalidFieldOrValueException(SanicException):
    status_code = 400
