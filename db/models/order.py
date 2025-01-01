from sqlalchemy import Integer, Column, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship

from db.db_setup import Base
from .mixins import TimeStamp
from enum import Enum as PyEnum
 
class OrderStatusEnum(str, PyEnum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"

class Order(Base, TimeStamp):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)