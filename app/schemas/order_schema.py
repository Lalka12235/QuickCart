from pydantic import BaseModel, Field

class OrderProductItem(BaseModel):
    #product_id: int
    title_product: str
    quantity: int = Field(1, description="Quantity of product")

class OrderSchema(BaseModel):
    address: str = Field(description='Your address for delivery')
    #delivered: bool = Field(False, description="Delivery status, default is False")
    products: list[OrderProductItem] = Field(..., description="List of products in the order")