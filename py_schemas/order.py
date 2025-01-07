from pydantic import BaseModel

from typing import List, Optional
from enum import Enum

from datetime import datetime

class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price_per_unit: float

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None

class OrderItemResponse(BaseModel):
    id: int
    product_name: str
    quantity: int
    price_per_unit: float

class OrderCreate(BaseModel):
    total_price: Optional[float] = None
    status: OrderStatusEnum = OrderStatusEnum.PENDING
    order_items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: str = None
    
class OrderUpdateResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: OrderStatusEnum

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: OrderStatusEnum
    created_at: datetime
    updated_at: datetime
    order_items: List[OrderItemResponse]

    class Config:
        orm_mode = True