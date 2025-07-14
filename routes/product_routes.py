from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.database import get_collection
from models.Product import Product
from app.utils.objectid_helper import object_id
from pathlib import Path
import shutil
from fastapi import Query

router = APIRouter()
product_collection = get_collection("products")
category_collection = get_collection("categories")

UPLOAD_DIR = Path("static/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Create product with image


@router.post("/post", response_model=Product)
def create_product(
    name: str = Form(...),
    price: float = Form(...),
    category_id: str = Form(...),
    image: UploadFile = File(...)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    if not category_collection.find_one({"_id": object_id(category_id)}):
        raise HTTPException(status_code=400, detail="Invalid category_id")

    filename = Path(image.filename).name
    image_path = UPLOAD_DIR / filename

    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    image_url = f"/static/images/{filename}"
    product = {
        "name": name,
        "price": price,
        "category_id": category_id,
        "image_url": image_url,
    }

    result = product_collection.insert_one(product)
    product["_id"] = str(result.inserted_id)
    return Product(**product)

# Get all products


@router.get("/getAll", response_model=list[Product])
def get_products():
    products = []
    for doc in product_collection.find():
        doc["_id"] = str(doc["_id"])
        products.append(Product(**doc))
    return products

# Get single product by ID


@router.get("/get/{id}", response_model=Product)
def get_product(id: str):
    _id = object_id(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid ID")

    product = product_collection.find_one({"_id": _id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product["_id"] = str(product["_id"])
    return Product(**product)

# Update product (optional image)


@router.put("/update/{id}", response_model=Product)
def update_product(
    id: str,
    name: str = Form(...),
    price: float = Form(...),
    category_id: str = Form(...),
    image: UploadFile = File(None)
):
    _id = object_id(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid ID")

    if not category_collection.find_one({"_id": object_id(category_id)}):
        raise HTTPException(status_code=400, detail="Invalid category_id")

    update_data = {
        "name": name,
        "price": price,
        "category_id": category_id,
    }

    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid image file")

        filename = Path(image.filename).name
        image_path = UPLOAD_DIR / filename

        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)
        update_data["image_url"] = f"/static/images/{filename}"

    result = product_collection.update_one({"_id": _id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    updated = product_collection.find_one({"_id": _id})
    updated["_id"] = str(updated["_id"])
    return Product(**updated)

# Delete product


@router.delete("/delete/{id}")
def delete_product(id: str):
    _id = object_id(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = product_collection.delete_one({"_id": _id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"detail": "Product deleted successfully"}


@router.get("/search")
def search_products(name: str = Query("", alias="name")):
    # Use `name` for filtering or return all if empty
    if name:
        results = product_collection.find(
            {"name": {"$regex": name, "$options": "i"}})
    else:
        results = product_collection.find()
    return [{**r, "_id": str(r["_id"])} for r in results]
