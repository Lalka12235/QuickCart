from pydantic import BaseModel, Field

class Order(BaseModel):
    title: str = Field(..., description="Order title")
    description: str = Field(..., description="Order description")
    price: int = Field(..., gt=0, description="Order price (positive integer)")
    delivered: bool = Field(False, description="Delivery status, default is False")


class UpdateOrder(BaseModel):
    delivered: bool | None = Field(None, description="Updated delivery status")