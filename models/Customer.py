from typing import Optional
from pydantic import BaseModel


class Customer(BaseModel):
    customer_id: Optional[str] = None
    name: str
    phone: str
    address: str
