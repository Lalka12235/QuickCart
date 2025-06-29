from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    title: str = Field(..., description="Product title")
    description: str = Field(..., description="Product description")
    price: int = Field(..., gt=0, description="Product price (must be positive)")
    quantity: int = Field(1, ge=0, description="Product quantity in stock (non-negative)")


class UpdateProductSchema(BaseModel):
    title: str | None = Field(None, description="Product title for update")
    description: str | None = Field(None, description="Product description for update")
    price: int | None = Field(None, gt=0, description="Product price for update (must be positive)")
    quantity: int | None = Field(None, ge=0, description="Product quantity for update (non-negative)")
