from pydantic import BaseModel
from typing import List
from datetime import datetime

"""Cart  Model"""

class CartCreate(BaseModel):
    user_id: int

class CartResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    items: List["CartItemResponse"]

    class Confid:
        orm_mode = True

# Cart Item Schema
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    quantity : int
    product_name: str
    product_price: float
    total_price: float

    class Config:
        orm_mode =True