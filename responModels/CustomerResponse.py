from pydantic import BaseModel

class CustomerResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
