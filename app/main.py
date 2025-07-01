from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.user_router import user
from app.api.v1.product_router import product
from app.api.v1.order_router import order
from app.api.v1.review_router import review


app = FastAPI(
    title='Online store',
    description='API for managing online store'
)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080/docs",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)


app.include_router(user)
app.include_router(product)
app.include_router(order)
app.include_router(review)