from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship

from db.db_setup import Base
from .mixins import TimeStamp


class Product(Base, TimeStamp):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    cart_items = relationship("Cart", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")