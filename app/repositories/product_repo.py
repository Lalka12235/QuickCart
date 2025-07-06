from sqlalchemy import select,update,delete,func
from app.config.session import Session
from app.models.product_model import ProductModel
from app.schemas.product_schema import ProductSchema
from typing import Any


class ProductRepository:

    @staticmethod
    def get_one_product_by_title(title: str) -> ProductModel | None:
        with Session() as session:
            stmt = select(ProductModel).where(ProductModel.title == title)
            result = session.execute(stmt)
            return result.scalar_one_or_none()
        

    @staticmethod
    def get_all_product() -> list[ProductModel]:
        with Session() as session:
            stmt = select(ProductModel)
            result = session.execute(stmt)
            return result.scalars().all()
        

    @staticmethod
    def add_product(product: ProductSchema) -> ProductModel:
        with Session() as session:
            new_product = ProductModel(
                title=product.title,
                description=product.description,
                price=product.price,
                quantity=product.quantity,
            )

            session.add(new_product)
            session.commit()
            session.refresh(new_product)
            return new_product

    @staticmethod
    def update_product(title: str, product: dict[str,Any]) -> bool:
        with Session() as session:
            stmt = (
                update(ProductModel)
                .where(ProductModel.title == title)
                .values(**product)
            )
            result = session.execute(stmt)
            session.commit()
            stmt_select = select(ProductModel).where(ProductModel.title == product.get('title', title))
            updated_product = session.execute(stmt_select).scalar_one_or_none()
            return updated_product 
    

    @staticmethod
    def delete_product(title: str) -> bool:
        with Session() as session:
            stmt = delete(ProductModel).where(ProductModel.title == title)
            session.execute(stmt)
            session.commit()
            return True


    @staticmethod
    def get_products_paginated(
        offset: int = 0, 
        limit: int = 10
    ) -> list[ProductModel]:
        with Session() as session:
            stmt = select(ProductModel).offset(offset).limit(limit)
            result = session.execute(stmt)
            return result.scalars().all()
        

    @staticmethod
    def update_quantity(product_id: int,delta: int) -> bool:
        with Session() as session:
            stmt = update(ProductModel).where(
                ProductModel.id == product_id,
            ).values(quantity=ProductModel.quantity + delta)
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0
        

    @staticmethod
    def get_total_products_count() -> int:
        with Session() as session:
            stmt = select(func.count(ProductModel.id))
            result = session.execute(stmt)
            return result.scalar()
        
    
