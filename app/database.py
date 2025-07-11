from pymongo import MongoClient

client = MongoClient("mongodb+srv://monodbuser:hcKDUVZ07AdNITEb@cluster0.s4cq9r5.mongodb.net/matching-directory?retryWrites=true&w=majority")
db = client["Flash_Light"]


def get_collection(name: str):
    return db[name]
