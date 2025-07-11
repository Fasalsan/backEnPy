from fastapi import APIRouter, HTTPException
from app.database import get_collection
from models.Product import Product
from app.utils.objectid_helper import object_id

router = APIRouter()
product_collection = get_collection("products")
category_collection = get_collection("categories")

@router.post("/post", response_model=Product)
def create_product(product: Product):
    category = category_collection.find_one({"_id": object_id(product.category_id)})
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")
    product_collection.insert_one(product.dict())
    return product

@router.get("/getAll")
def get_products():
    return [doc | {"_id": str(doc["_id"])} for doc in product_collection.find()]

@router.get("/get/{id}", response_model=Product)
def get_product(id: str):
    _id = object_id(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    product = product_collection.find_one({"_id": _id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product["product_id"] = str(product["_id"])
    product.pop("_id", None)
    return product


@router.put("/update/id={id}", response_model=Product)
def update_product(id: str, product: Product):
    _id = object_id(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid ID")
    category = category_collection.find_one({"_id": object_id(product.category_id)})
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")
    result = product_collection.update_one({"_id": _id}, {"$set": product.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/delete/id={id}")
def delete_product(id: str):
    _id = object_id(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = product_collection.delete_one({"_id": _id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}
