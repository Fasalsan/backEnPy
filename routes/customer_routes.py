from fastapi import APIRouter, HTTPException
from typing import List
from app.database import get_collection
from models.Customer import Customer
from app.utils.objectid_helper import object_id

router = APIRouter()
collection = get_collection("customers")


@router.post("/post", response_model=Customer)
def create_customer(customer: Customer):
    data = customer.dict(by_alias=True, exclude={"customer_id", "id"})
    try:
        # collection must be a MongoDB collection object
        result = collection.insert_one(data)
        saved_customer = customer.dict()
        saved_customer["customer_id"] = str(result.inserted_id)
        return saved_customer
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error inserting customer: {e}")


@router.get("/getAll", response_model=List[Customer])
def get_customers():
    customers = [
        {
            **{k: v for k, v in doc.items() if k != "_id"},
            "customer_id": str(doc["_id"]),
            "id": str(doc["_id"]),
        }
        for doc in collection.find()
    ]
    return customers


@router.get("/get/{id}", response_model=Customer)
def get_customer(id: str):
    _id = object_id(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid ID")

    customer = collection.find_one({"_id": _id})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer["customer_id"] = str(customer["_id"])
    customer["id"] = str(customer["_id"])
    customer.pop("_id", None)
    return customer


@router.put("/update/id={id}", response_model=Customer)
def update_customer(id: str, customer: Customer):
    _id = object_id(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid ID")

    data = customer.dict(exclude={"customer_id", "id"})
    result = collection.update_one({"_id": _id}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")

    updated_customer = collection.find_one({"_id": _id})
    updated_customer["customer_id"] = str(updated_customer["_id"])
    updated_customer["id"] = str(updated_customer["_id"])
    updated_customer.pop("_id", None)
    return updated_customer


@router.delete("/delete/id={id}")
def delete_customer(id: str):
    _id = object_id(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = collection.delete_one({"_id": _id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {"detail": "Customer deleted"}


@router.get("/getByPhone={phone}", response_model=Customer)
def get_customer_by_phone(phone: str):
    customer = collection.find_one({"phone": phone})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer["customer_id"] = str(customer["_id"])
    customer["id"] = str(customer["_id"])
    customer.pop("_id", None)
    return customer


@router.get("/getByName={name}", response_model=List[Customer])
def get_customer_by_name(name: str):
    customers = collection.find({"name": {"$regex": name, "$options": "i"}})
    result = [
        {
            **{k: v for k, v in doc.items() if k != "_id"},
            "customer_id": str(doc["_id"]),
            "id": str(doc["_id"]),
        }
        for doc in customers
    ]
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return result
