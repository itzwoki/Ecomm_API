from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.orm import Session
from db.db_setup import get_db
from db.models.cart import Cart
from db.models.CartItem import CartItem
from py_schemas.cart import CartResponse, CartItemCreate, CartItemUpdate
from userRoutes.dependencies.currentUser import get_current_user
from .utils import add_to_cart, update_cart_item, remove_item, clear_cart, get_all

router = APIRouter(prefix="/cart")

@router.post("/add-to-cart")
async def add_item_to_cart(
    item: CartItemCreate,
    db: Session =  Depends(get_db),
    current_user : dict = Depends(get_current_user)
):
    user_id = current_user.id

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized.")
    
    product_id = item.product_id
    quantity = item.quantity
    
    return await add_to_cart(user_id, db, product_id, quantity)

@router.patch("/update/{product_id}")
async def update_item_in_cart(
    product_id: int,
    item : CartItemUpdate,
    db: Session = Depends(get_db),
    current_user : dict = Depends(get_current_user)
):
    user_id = current_user.id

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Un-Authorized.")
    
    new_quantity = item.quantity

    return await update_cart_item(user_id, product_id, new_quantity, db)
    
@router.delete("/delete/{product_id}")
async def delete_item_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.id

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized.")
    
    return await remove_item(product_id, user_id, db)

@router.delete("/Empty-Cart")
async def Empty_cart(
    db: Session = Depends(get_db),
    current_user : dict = Depends(get_current_user)
):
    user_id = current_user.id

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    return await clear_cart(user_id, db)


@router.get("/", response_model=CartResponse)
async def get_whole_cart(
    db: Session = Depends(get_db),
    current_user : dict = Depends(get_current_user)
):
    user_id = current_user.id

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    return await get_all(user_id, db)