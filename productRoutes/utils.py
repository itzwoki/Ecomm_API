from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from db.models.product import Product
from py_schemas.product import ProductCreate, ProductUpdate


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