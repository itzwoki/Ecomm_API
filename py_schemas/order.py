from pydantic import BaseModel

from typing import List, Optional
from enum import Enum

from datetime import datetime

class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"

class OrderCreate(BaseModel):
    total_price: float
    status: OrderStatusEnum = OrderStatusEnum.PENDING
    order_items: List[int]

class OrderUpdate(BaseModel):
    total_price : Optional[float] = None
    status : Optional[OrderStatusEnum] = None
    order_items : Optional[List[int]] = None

class OrderItemResponse(BaseModel):
    id: int
    quantity : int
    price_per_unit: float

class OrderResponse(BaseModel):
    id: int
    user_id : int
    total_price : float
    status: OrderStatusEnum
    created_at : datetime
    updated_at: datetime

    class Config:
        orm_mode = True