from sqlalchemy import Column, Integer, Float, String , Enum, ForeignKey
from sqlalchemy.orm import relationship

from enum import Enum as PyEnum

from db.db_setup import Base
from .mixins import TimeStamp

class PaymentStatus(PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class PaymentMethod(PyEnum):
    STRIPE = "stripe"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"

class Payment(Base, TimeStamp):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_id = Column(String, unique=True ,nullable=False)
    amount = Column(Float, nullable=False)

    order = relationship("Order", back_populates="payment")

