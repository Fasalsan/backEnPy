from fastapi import APIRouter, HTTPException
from app.database import get_collection
from models.Customer import Customer
from app.utils.objectid_helper import object_id

router = APIRouter()
collection = get_collection("customers")


@router.post("/post", response_model=Customer)
def create_customer(customer: Customer):
    result = collection.insert_one(customer.dict(by_alias=True, exclude={"customer_id"}))
    saved_customer = customer.dict()
    saved_customer["customer_id"] = str(result.inserted_id)
    return saved_customer



@router.get("/getAll")
def get_customers():
    return [
        {
            **{k: v for k, v in doc.items() if k != "_id"},
            "customer_id": str(doc["_id"])
        }
        for doc in collection.find()
    ]



@router.get("/get/{id}")
def get_customer(id: str):
    _id = object_id(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid ID")

    customer = collection.find_one({"_id": _id})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer["customer_id"] = str(customer["_id"])
    customer.pop("_id", None)
    return customer


@router.put("/update/{id}", response_model=Customer)
def update_customer(id: str, customer: Customer):
    _id = object_id(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = collection.update_one(
        {"_id": _id}, {"$set": customer.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


@router.delete("/delete/{id}")
def delete_customer(id: str):
    _id = object_id(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = collection.delete_one({"_id": _id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {"detail": "Customer deleted"}


@router.get("/getByPhone/{phone}")
def get_customer_by_phone(phone: str):
    customer = collection.find_one({"phone": phone})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer["customer_id"] = str(customer["_id"])
    customer.pop("_id", None)
    return customer
