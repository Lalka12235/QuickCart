from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.handlers.order_router import order
from app.handlers.product_router import product
from app.handlers.user_router import user
from app.auth.auth import auth

app = FastAPI(
    title='Online stor',
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
app.include_router(auth)