from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional

from db.db_setup import get_db
from userRoutes.dependencies.currentUser import get_current_user
from py_schemas.order import OrderUpdate
from py_schemas.payment import PaymentRequest
from .utils import convert_cart_to_order, up_order

router = APIRouter(prefix="/order")

@router.post("/Make_order", description="Convert Your Cart to Order")
async def make_order(
    order_request: PaymentRequest,
    card_details: Optional[dict] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) 
):
    user_id = current_user.id
    payment_method = order_request.payment_method
    try:
        order_response = await convert_cart_to_order(user_id, payment_method,card_details, db)
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