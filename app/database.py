from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["testing_db"]


def get_collection(name: str):
    return db[name]
