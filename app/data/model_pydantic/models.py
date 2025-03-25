from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Order(BaseModel):
    title:str
    description:str
    price:int
    delivered: bool = False


class Product(BaseModel):
    title:str
    description:str
    price:int


class UpdateProduct(Product):
    pass

class UpdateOrder(Order):
    pass

class ReviewsModel(BaseModel):
    username: str
    title: str
    description: str
