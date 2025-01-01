from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional


from db.db_setup import get_db
from userRoutes.dependencies.currentUser import check_admin, get_current_user
from .utils import product_create, get_products, get_product, search_name, product_update, del_pro_by_id, get_pro_by_cat, filter_product, apply_discount
from py_schemas.product import ProductCreate, ProductResponse, ProductUpdate, DiscountedProductResponse, DiscountRequest

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

@router.patch("/update-product/{product_id}", response_model=ProductResponse)
async def update_product_by_id(
        product_id : int,
        product: ProductUpdate,
        db: Session = Depends(get_db),
        current_admin : dict = Depends(check_admin)
):
    id = current_admin.id
    if not id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission Denied"
        )
    return await product_update(product_id, product, db)

@router.delete("/delete-by-id/{product_id}")
async def delete_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: dict =  Depends(check_admin)
):
    id = current_admin.id

    if not id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized.")
    
    return await del_pro_by_id(product_id, db)

@router.get("/get-by-category/{category_name}", description="Get All Products for given category")
async def get_by_category(
    category_name: str,
    db: Session = Depends(get_db),
    current_user : dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized.")
    return await get_pro_by_cat(category_name, db)

@router.get(
"/filter-products",
description="Filter Products by category and price",)

async def products_filter(
    db: Session = Depends(get_db),
    current_user : dict = Depends(get_current_user),
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 20
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized.")
    
    return await filter_product(db, category, min_price, max_price, skip, limit)

@router.patch("/apply-discount/{product_id}", description="Apply discount to a product", response_model=DiscountedProductResponse)
async def apply_discount_route(
    product_id: int,
    discount_request : DiscountRequest,
    db: Session = Depends(get_db),
    current_admin: dict =  Depends(check_admin)
):
    id = current_admin.id

    if not id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized.")
    
    discount = discount_request.discount
    
    return await apply_discount(db, product_id, discount)