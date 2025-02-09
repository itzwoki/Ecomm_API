from pydantic import BaseModel, Field
from typing import Optional
 
from datetime import datetime

class ProductCreate(BaseModel):
    name : str
    description: Optional[str] = None
    price : float
    stock : int = 0
    category : Optional[str] = None
    image_url : Optional[str] = None


class ProductUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    price : Optional[float] = None
    stock: Optional[int] = None
    category : Optional[str] = None
    image_url : Optional[str] = None

class DiscountRequest(BaseModel):
    discount: float
    duration: Optional[int] = 24

class ProductResponse(BaseModel):
    id: int
    name : str
    price : float
    stock : int = 0
    created_at : datetime
    updated_at: datetime
    discount_percentage: Optional[float] = 0.0
    discounted_price: float = Field(default=0.0)

class DiscountedProductResponse(ProductResponse):
    discount_percentage: Optional[float] = 0.0
    discounted_price: float


    class Config:
        orm_mode = True