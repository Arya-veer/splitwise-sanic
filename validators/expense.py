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
        if "amount" not in payload:
            raise IncompleteParametersException("'amount' not provided")
        total_amount = payload.get("amount")
        if "users" not in payload:
            raise IncompleteParametersException("'users' not provided")
        pos_amount = neg_amount = 0
        for user in payload.get("users"):
            if "user_id" not in user:
                raise IncompleteParametersException("'user_id' not provided for user")
            if "amount" not in user:
                raise IncompleteParametersException("'amount' not provided for user")
            if "has_paid" not in user:
                raise IncompleteParametersException("'has_paid' not provided for user")
            if user.get("has_paid"):
                pos_amount += user.get("amount")
            else:
                neg_amount += user.get("amount")
        if total_amount != pos_amount or total_amount != neg_amount:
            raise SanicException("Amounts do not match")

    @staticmethod
    def validate_rename_expense(payload):
        if "title" not in payload:
            raise IncompleteParametersException("'title' not provided")
