from sqlalchemy.orm import Session
from sqlalchemy import func

from fastapi import HTTPException, status
from typing import Optional

from db.models.product import Product
from py_schemas.product import ProductCreate, ProductUpdate
from datetime import datetime


async def get_products(
        db: Session
):
    all_products = db.query(Product).all()

    return all_products

async def get_product(
        product_id: int,
        db: Session
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID: {product_id} doesn't exist.")
    return product

async def search_name(
        product_name: str,
        db: Session
):
    product_name = product_name.strip()
    products = db.query(Product).filter(Product.name.ilike(f"%{product_name}%")).all()

    print(f"Searching for: {product_name}")
    print(f"Products found: {products}")

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No Product with the name containing: {product_name}"
        )
    
    
    return products

async def product_create(
        product : ProductCreate,
        db: Session 
):
    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with same name already exist."
        )
    
    new_product = Product(
        name = product.name,
        description = product.description,
        price = product.price,
        stock = product.stock,
        category = product.category,
        image_url = product.image_url
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

async def product_update(
        product_id: int,
        productup : ProductUpdate,
        db: Session
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No Product with the ID: {product_id}."
        )
    
    update_data = productup.model_dump(exclude_unset=True)  # Get only fields that are set
    for field, value in update_data.items():
        setattr(product, field, value)

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

async def del_pro_by_id(
        product_id : int,
        db: Session
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID: {product_id} doesn't exist."
        )
    if product:
        db.delete(product)
        db.commit()
        
        return {
            "message" : "Product Deleted Successfully." 
        }
    
async def get_pro_by_cat(
        category_name : str,
        db: Session
):
    products = db.query(Product).filter(Product.category == category_name).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Products for given category.")
    
    return products

async def filter_product(
        db: Session,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        skip: int = 0,
        limit: int = 20,
):
    query = db.query(Product)

    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Min Price Cannot be greater than Max Price.    ")

    if category:
        query = query.filter(Product.category == category)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    products = query.offset(skip).limit(limit).all()

    return products

async def apply_discount(
        db: Session,
        product_id: int,
        discount: float,
        duration: int
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not Found.")
    
    if not (0 <= discount <=100 ):
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discount Perecntage must be between 0 AND 100."
        )
    
    product.discount_percentage = discount
    product.discount_start_time = datetime.now()
    product.discount_duration = duration

    db.commit()
    db.refresh(product)
    return product

async def low_stock(
        db: Session,
        stock_limit: int = 10,
        skip: int = 0,
        limit : int = 4
):
    results = (
        db.query(
            Product.id,
            Product.name,
            func.sum(Product.stock).label("Total_stock")
        )
        .filter(Product.stock < stock_limit)
        .group_by(Product.id, Product.name) 
        .offset(skip)
        .limit(limit)
        .all()
    )

    if not results:
        return {"message" : f"No Product with Stock less than {stock_limit}"}
    
    return [
        {
            "Product-ID" : result.id, 
            "Category" : result.name,
            "Total_stock" : result.Total_stock
        }
        for result in results
    ]
