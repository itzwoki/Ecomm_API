from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.db_setup import Base
from .mixins import TimeStamp

class Cart(Base, TimeStamp):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    
    user = relationship("User", back_populates="carts") #relation with user
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan") # relation with cart items