from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    product_id: Optional[str] = Field(None, alias="_id")
    name: str
    price: float
    # cost: float
    # qty: float
    category_id: str
    category_name: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        by_alias = True
