from pydantic import BaseModel, field_validator

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
    CASH_ON_DELIVERY = "cash_on_delivery"

class PaymentRequest(BaseModel):
    payment_method: PaymentMethodEnum

    @field_validator('payment_method')
    def validate_payment_method(cls, v):
        return v.lower()


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