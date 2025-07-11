from pydantic import BaseModel, Field

class Sale(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)
    customer_phone: str
