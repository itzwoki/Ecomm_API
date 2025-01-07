from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from datetime import datetime

from db.models.cart import Cart
from db.models.payment import Payment
from db.models.CartItem import CartItem
from db.models.order_item import OrderItem
from db.models.order import Order, OrderStatusEnum
from userRoutes.dependencies.payment import process_payment

async def convert_cart_to_order(user_id: int, payment_method: str,card_details: dict, db: Session):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart or not cart.items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is Empty.")
    
    total_price = sum(item.quantity * item.product.price for item in cart.items)

    # Processing Payment from  "from userRoutes.dependencies.payment import process_payment"
    payment_status = await process_payment(payment_method, card_details, total_price)

    # Creating Order
    new_order = Order(
        user_id=user_id,
        total_price=total_price,
        status=OrderStatusEnum.PENDING
    )

    db.add(new_order)
    db.flush()

    # Creating Order Items
    for cart_item in cart.items:
        new_order_item = OrderItem(
            order_id=new_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price_per_unit=cart_item.product.price
        )
        db.add(new_order_item)

    # Creating Payment record
    payment = Payment(
        order_id=new_order.id,
        payment_method=payment_method,  # Can be 'CASH_ON_DELIVERY', 'ONLINE_PAYMENT', etc.
        payment_status=payment_status,  # Paymentstatus from process payment
        transaction_id=f"{payment_method}-{new_order.id}-{int(datetime.now().timestamp())}",
        amount=total_price
    )

    db.add(payment)

    # clearing the cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()

    return {
        "message": "Order created successfully.",
        "order": {
            "id": new_order.id,
            "user_id": new_order.user_id,
            "total_price": new_order.total_price,
            "status": new_order.status,
            "payment_status": payment.payment_status,  
            "payment_method": payment.payment_method,  
            "transaction_id": payment.transaction_id,  
            "items": [
                {
                    "id": order_item.id,
                    "product_id": order_item.product_id,
                    "quantity": order_item.quantity,
                    "price_per_unit": order_item.price_per_unit
                }
                for order_item in new_order.order_items
            ]
        }
    }


async def up_order(user_id: int, db: Session, stat: str):
    order = db.query(Order).filter(Order.user_id == user_id).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Order Exists yet.")
    
    order.status = stat
    db.commit()
    db.refresh(order)

    return {
        "message": "Order status updated successfully.",
        "order": {
            "id": order.id,
            "user_id": order.user_id,
            "total_price": order.total_price,
            "status": order.status,
        }
    }

