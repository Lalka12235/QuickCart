from pydantic import BaseModel

class ProductSchema(BaseModel):
    title:str
    description:str
    price:int
    quantity: int


class UpdateProductSchema(BaseModel):
    price:int
    quantity: int