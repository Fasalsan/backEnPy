from fastapi import APIRouter, HTTPException
from app.database import get_collection
from models.Sale import Sale
from app.utils.objectid_helper import object_id
from pymongo import ReturnDocument

router = APIRouter()

product_collection = get_collection("products")
customer_collection = get_collection("customers")
sales_collection = get_collection("sales")


@router.post("/sale/create")
def create_sale_order(sale: Sale):
    product_id = object_id(sale.product_id)
    if not product_id:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product = product_collection.find_one({"_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    customer = customer_collection.find_one({"phone": sale.customer_phone})

    # Auto-create customer if not found
    if not customer:
        new_customer = {
            "name": "Unknown",  # or get from sale if you extend model
            "phone": sale.customer_phone,
            "address": ""
        }
        insert_result = customer_collection.insert_one(new_customer)
        customer = customer_collection.find_one(
            {"_id": insert_result.inserted_id})

    updated_product = product_collection.find_one_and_update(
        {"_id": product_id, "qty": {"$gte": sale.quantity}},
        {"$inc": {"qty": -sale.quantity}},
        return_document=ReturnDocument.AFTER
    )
    if not updated_product:
        raise HTTPException(status_code=400, detail="Not enough stock")

    sales_collection.insert_one({
        "product_id": str(product["_id"]),
        "product_name": product["name"],
        "category_id": product["category_id"],
        "price": product["price"],
        "quantity": sale.quantity,
        "total": product["price"] * sale.quantity,
        "customer_name": customer["name"],
        "customer_phone": customer["phone"],
        # "created_at": datetime.utcnow()
    })

    return {
        "detail": "Sale order created successfully",
        "product": product["name"],
        "quantity": sale.quantity,
        "remaining_stock": updated_product["qty"],
        "customer": customer["name"]
    }


@router.get("/sales")
def get_all_sales():
    sales = list(sales_collection.find())
    # Convert ObjectId to string and datetime to isoformat for JSON serializable
    for sale in sales:
        sale["_id"] = str(sale["_id"])
        if "created_at" in sale:
            sale["created_at"] = sale["created_at"].isoformat()
    return sales


@router.get("/sales/by-customer/{phone}")
def get_sales_by_customer_phone(phone: str):
    sales = list(sales_collection.find({"customer_phone": phone}))

    if not sales:
        raise HTTPException(
            status_code=404, detail="No sales found for this customer")

    # Format ObjectId and datetime
    for sale in sales:
        sale["_id"] = str(sale["_id"])
        if "created_at" in sale:
            sale["created_at"] = sale["created_at"].isoformat()

    return sales
