from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from db.db_setup import get_db
from userRoutes.dependencies.currentUser import check_admin, get_current_user
from py_schemas.order import OrderCreate, OrderResponse, OrderItemCreate, OrderItemResponse, OrderUpdate, OrderItemUpdate, OrderStatusEnum
from .utils import convert_cart_to_order

router = APIRouter(prefix="/order")

@router.post("/Make_order", description="Convert Your Cart to Order")
async def make_order(
    current_user : dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    try: 
        order_response = await convert_cart_to_order(user_id, db)
        return order_response
    except HTTPException as e:
        raise e
