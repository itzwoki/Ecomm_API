from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from db.db_setup import Base
from .mixins import TimeStamp

class OrderItem(Base, TimeStamp):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price_per_unit = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")