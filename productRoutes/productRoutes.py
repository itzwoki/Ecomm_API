from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List


from db.db_setup import get_db
from userRoutes.dependencies.currentUser import check_admin, get_current_user
from .utils import product_create, get_products, get_product, search_name
from py_schemas.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/products")

@router.post("/", response_model=ProductResponse)
async def create_product(
    product : ProductCreate,
    db: Session = Depends(get_db),
    current_admin : dict = Depends(check_admin)
):
    id = current_admin.id
    if not id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission Denied"
        )
    
    new_product = await product_create(product, db)
    return ProductResponse(
        id=new_product.id,
        name=new_product.name,
        price=new_product.price,
        stock=new_product.stock,
        created_at=new_product.created_at,
        updated_at=new_product.updated_at
    )

@router.get("/get-all-products", response_model=List[ProductResponse])
async def get_all_products(
    db: Session = Depends(get_db),
    user_id : dict = Depends(get_current_user)
):
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authrorized.")
    return await get_products(db)

@router.get("/get-product/{product_id}", response_model=ProductResponse)
async def get_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin : dict = Depends(check_admin)
):
    id = current_admin.id
    if not id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission Denied"
        )
    return await get_product(product_id,db)

@router.get("/search-name/{product_name}", response_model=List[ProductResponse])
async def search_by_name(
    product_name: str,
    db : Session = Depends(get_db),
    user_id : dict = Depends(get_current_user)
):
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authrorized.")
    return await search_name(product_name, db)