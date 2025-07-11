from pydantic import BaseModel, Field

class Customer(BaseModel):
    customer_id: str = Field(default=None, alias="_id")
    name: str
    phone: str

    class Config:
        allow_population_by_field_name = True
