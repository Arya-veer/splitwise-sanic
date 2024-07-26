from typing import List
from tortoise.queryset import QuerySet

class UserSerializer:

    @staticmethod
    def serialize_users(qs:QuerySet):
        data = []
        for obj in qs:
            serialized_obj = {
                "static_id" : str(obj.static_id),
                "name": obj.name,
                "email" : obj.email
            }
            data.append(
                serialized_obj
            ) 
        return data

    @staticmethod
    def serialize_user(user):
        return {
            "static_id" : str(user.static_id),
            "name": user.name,
            "email" : user.email
        }