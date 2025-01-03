from fastapi import FastAPI

from db.db_setup import engine
from db.models import user,product, order, cart, order_item,payment, CartItem
from userRoutes.userRoutes import router as userRouter
from productRoutes.productRoutes import router as productRouter
from cartRoutes.cartRoutes import router as cartRouter


user.Base.metadata.create_all(bind=engine)
product.Base.metadata.create_all(bind=engine)
order.Base.metadata.create_all(bind=engine)
cart.Base.metadata.create_all(bind=engine)
CartItem.Base.metadata.create_all(bind=engine)
order_item.Base.metadata.create_all(bind=engine)
payment.Base.metadata.create_all(bind=engine)

app=FastAPI(
    title="E-Commerce",
description="E-Comm Backend.",
contact={
    "name": "M.Waqas",
    "email": "abdullahwaqas22@gmail.com"

},
license_info={
    "name": "Associate Software Engineer"
}
)

app.include_router(userRouter)
app.include_router(productRouter)
app.include_router(cartRouter)