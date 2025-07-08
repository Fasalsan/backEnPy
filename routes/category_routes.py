from fastapi import APIRouter, HTTPException
from app.database import get_collection
# from app.models.category import Category
from models.Category import Category
from app.utils.objectid_helper import object_id

router = APIRouter()
collection = get_collection("categories")

@router.post("/post", response_model=Category)
def create_category(category: Category):
    collection.insert_one(category.dict())
    return category

@router.get("/getAll")
def get_categories():
    return [doc | {"_id": str(doc["_id"])} for doc in collection.find()]
