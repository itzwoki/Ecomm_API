from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from db.models.cart import Cart
from db.models.CartItem import CartItem
from db.models.order_item import OrderItem
from db.models.order import Order, OrderStatusEnum

async def convert_cart_to_order(user_id : int, db: Session):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart or not cart.items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is Empty.")
    
    total_price = sum(item.quantity * item.product.price for item in cart.items)

    #Creating Order
    new_order = Order(
        user_id = user_id,
        total_price = total_price,
        status = OrderStatusEnum.PENDING
    )

    db.add(new_order)
    db.flush()

    #creating order Items 
    for cart_item in cart.items:
        new_order_item = OrderItem(
            order_id = new_order.id,
            product_id = cart_item.product_id,
            quantity = cart_item.quantity,
            price_per_unit = cart_item.product.price
        )
        db.add(new_order_item)

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()

    return {
        "message": "Order created successfully.",
        "order": {
            "id": new_order.id,
            "user_id": new_order.user_id,
            "total_price": new_order.total_price,
            "status": new_order.status,
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