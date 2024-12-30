from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.db_setup import Base
from .mixins import TimeStamp

class Cart(Base, TimeStamp):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    user = relationship("User", back_populates="carts")
    product = relationship("Product", back_populates="cart_items")