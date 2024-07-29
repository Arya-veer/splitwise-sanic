class GroupSerializer:

    @staticmethod
    def serialize_groups(qs):
        data = []
        for obj in qs:
            serialized_obj = {
                "static_id": str(obj.static_id),
                "name": obj.name,
                "created_at": obj.created_at.strftime("%d %B, %Y"),
            }
            data.append(serialized_obj)
        return data

    @staticmethod
    def serialize_group(obj):
        return {
            "static_id": str(obj.static_id),
            "name": obj.name,
            "created_at": obj.created_at.strftime("%d %B, %Y"),
        }
