from typing import List, Optional
from pydantic import BaseModel

class CartItem(BaseModel):
    name: str
    quantity: int
    price: float
    description: Optional[str] = None
    person: Optional[str] = None

class CartData(BaseModel):
    restaurant: str
    items: List[CartItem]
    total_price: float 