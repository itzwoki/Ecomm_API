from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship

from db.db_setup import Base
from .mixins import TimeStamp
from datetime import timedelta, datetime


class Product(Base, TimeStamp):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    discount_percentage = Column(Float, default=0.0)
    discount_start_time = Column(DateTime, nullable=True)
    discount_duration = Column(Integer, nullable=True)

    @property
    def discounted_price(self):
        """Calculate the Price After Applying Discount."""
        return round(self.price * (1 - self.discount_percentage / 100), 2)
    
    def is_discount_active(self):
        """"Check if discount is still vvalid."""
        if self.discount_start_time and self.discount_duration:
            expiration_time = self.discount_start_time + timedelta(hours = self.discount_duration)
            return datetime.now() < expiration_time
        return False

    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")