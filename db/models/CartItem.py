from sqlalchemy import Column, Integer, ForeignKey

from sqlalchemy.orm import relationship

from db.db_setup import Base
from .mixins import TimeStamp

class CartItem(TimeStamp, Base):
    __tablename__ = "cartitems"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("Cart", back_populates="items") #relation with Cart Model.
    product = relationship("Product", back_populates="cart_items") #Relation with Product Model.