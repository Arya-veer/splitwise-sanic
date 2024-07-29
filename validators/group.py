from exceptions import IncompleteParametersException


class GroupValidator:

    @staticmethod
    def validate_create_group(payload):
        if "group_name" not in payload:
            raise IncompleteParametersException()

    @staticmethod
    def validate_add_users(payload):
        if "emails" not in payload:
            raise IncompleteParametersException()
        if len(payload["emails"]) == 0:
            raise IncompleteParametersException()
