from bson import ObjectId


def object_id(id: str):
    try:
        return ObjectId(id)
    except:
        return None
