from bson import ObjectId

def object_id(id_str):
    try:
        return ObjectId(id_str)
    except:
        return None
