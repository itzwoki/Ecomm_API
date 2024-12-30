from pydantic import BaseModel
from typing import List


class CartCreate(BaseModel):
    product_id : int
    quantity : int

class CartItemResponse(BaseModel):
    product_id: int
    product_name: str
    product_price: float
    quantity: int

class CartResponse(BaseModel):
    user_id: int
    items: List[CartItemResponse]
    total_price: float

    class Config:
        orm_mode =True