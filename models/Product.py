from pydantic import BaseModel

class Product(BaseModel):
    
    name: str
    price: float
    category_id: str  # Reference to category
