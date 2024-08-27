from exceptions import IncompleteParametersException, SanicException


class ExpenseValidator:

    @staticmethod
    def validate_create_expense(payload, group, user):
        if group is None:
            raise IncompleteParametersException("Group not found")
        if user is None:
            raise IncompleteParametersException("User not found")
        if "title" not in payload:
            raise IncompleteParametersException("'title' not provided")
        if "split_type" not in payload:
            raise IncompleteParametersException("'title' not provided")
            

    @staticmethod
    def validate_rename_expense(payload):
        if "title" not in payload:
            raise IncompleteParametersException("'title' not provided")
