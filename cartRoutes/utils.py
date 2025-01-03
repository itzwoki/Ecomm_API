from sqlalchemy.orm import Session, joinedload


from fastapi import HTTPException, status

from db.models.cart import Cart
from db.models.CartItem import CartItem
from db.models.product import Product
from py_schemas.cart import CartResponse, CartItemResponse


#add a product to cart
#update item in cart
#get all item in cart
#remove product from cart
#clear cart



async def add_to_cart(
        #check if product exist --- #check if user has a cart if not create it -- #check if product is already in the cart if yes 
        # increase qunatity only -- if not add product 
        user_id: int,
        db: Session,
        product_id: int,
        quantity: int
):
    #checking if the product exist before entering to the cart and check if user has a cart if not create one
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product doesn't exist.")
    
    cart = db.query(Cart).filter(Cart.id == user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    cart_item = db.query(CartItem).filter(CartItem.product_id == product_id).first()

    if cart_item:
        cart_item.quantity += quantity
        db.commit()
        db.refresh(cart_item)

    else:
        new_cart_item = CartItem(cart_id = cart.id, product_id = product_id, quantity = quantity)
        db.add(new_cart_item)
        db.commit()
        db.refresh(new_cart_item)

    return { "message " : f"Added to cart!. "}

async def update_cart_item(
        user_id: int,
        product_id: int,
        new_quantity : int,
        db: Session
):
    cart_item = db.query(CartItem).join(Cart).filter(Cart.user_id == user_id, CartItem.product_id == product_id).first()

    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item now found in cart.")
    
    if new_quantity<=0:
        db.delete(cart_item)
        response = {"message" :"Item removed from Cart"}

    else:
        cart_item.quantity = new_quantity
        response = {"message" : "Cart Item updated" , "quantity" : cart_item.quantity}

        db.commit()
        return response
    
async def remove_item(
        product_id: int,
        user_id: int,
        db: Session 
):
    item = db.query(CartItem).join(Cart).filter(Cart.user_id == user_id, CartItem.product_id == product_id).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Is not in cart.")
    
    else:
        db.delete(item)
        db.commit()
        return{"message" : "Item Deleted from Cart."}
    
async def clear_cart(
        user_id: int,
        db: Session
):
    items = db.query(CartItem).join(Cart).filter(Cart.user_id == user_id).all()

    if not items:
        response = {"message" : "Cart is Already Empty."}
    for item in items:
        db.delete(item)
        db.commit()
        response = {"messaage": "All items have been removed from the cart."}
    

    return response

async def get_all(
        user_id: int,
        db: Session
)-> CartResponse:
    
    cart = db.query(Cart).options(joinedload(Cart.items).joinedload(CartItem.product)).filter(Cart.user_id == user_id).first()

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is Empty.")
    
    cart_response = CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        created_at=cart.created_at,
        updated_at=cart.updated_at,
        items=[
            CartItemResponse(
                id=item.id,
                cart_id=item.cart_id,
                quantity=item.quantity,
                product_name=item.product.name,
                product_price=item.product.price,
                total_price=item.quantity * item.product.price
            )
            for item in cart.items
        ]
    )

    return cart_response


    