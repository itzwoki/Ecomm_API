from pydantic import BaseModel

from enum import Enum

from datetime import datetime

class PaymentStatusEnum(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class PaymentMethodEnum(str, Enum):
    STRIPE = "stripe"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"

class PaymentCreate(BaseModel):
    order_id :int
    payment_method : PaymentMethodEnum
    transaction_id : str
    amount : float

class PaymentUpdate(BaseModel):
    payment_method : PaymentMethodEnum
    payment_status: PaymentStatusEnum
    transaction_id : str
    amount : float

class PaymentResponse(BaseModel):
    id : int
    order_id : int
    payment_method: PaymentMethodEnum
    payment_status : PaymentStatusEnum
    transaction_id : str
    amount : float
    created_at : datetime
    updated_at: datetime

    class Config:
        orm_mode = True