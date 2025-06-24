from pydantic import BaseModel

class Order(BaseModel):
    title:str
    description:str
    price:int
    delivered: bool = False


class UpdateOrder:
    devilered: bool