from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from db.db_setup import Base
from .mixins import TimeStamp
from enum import Enum as PyEnum


class UserRoleEnum(str, PyEnum):
    ADMIN = "admin"
    USER = "user"

class User(Base, TimeStamp):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRoleEnum, name="userrole_enum"), default=UserRoleEnum.USER)

    carts = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")