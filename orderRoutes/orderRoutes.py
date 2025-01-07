from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from db.db_setup import get_db
from userRoutes.dependencies.currentUser import check_admin, get_current_user
from py_schemas.order import OrderUpdateResponse, OrderCreate, OrderResponse, OrderItemCreate, OrderItemResponse, OrderUpdate, OrderItemUpdate, OrderStatusEnum
from .utils import convert_cart_to_order, up_order

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

@router.patch("/update-status")
async def update_order_status(
    status : OrderUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.id

    try:
        order_status = await up_order(user_id, db,  status.status)
        return order_status
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update order status: {str(e)}"
        )