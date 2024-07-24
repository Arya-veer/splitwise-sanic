from typing import List
from tortoise.queryset import QuerySet
from models.group import Group

async def serialize_groups(qs):
    data = []
    for obj in qs:
        serialized_obj = {
            "static_id" : str(obj.static_id),
            "name" : obj.name,
            "created_at" : obj.created_at.strftime("%d %B, %Y")
        }
        data.append(
            serialized_obj
        )   
    return data 