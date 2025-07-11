from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    name: str
    category_id: str
    price: float
    qty: int  # stock quantity
    cost: float
