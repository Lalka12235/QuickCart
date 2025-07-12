from sqlalchemy import select,update,delete,func
from app.models.product_model import ProductModel
from app.schemas.product_schema import ProductSchema
from typing import Any
from sqlalchemy.orm import Session


class ProductRepository:

    @staticmethod
    def get_one_product_by_title(db: Session,title: str) -> ProductModel | None:
            stmt = select(ProductModel).where(ProductModel.title == title)
            result = db.execute(stmt)
            return result.scalar_one_or_none()
        

    @staticmethod
    def get_all_product(db: Session,) -> list[ProductModel]:
            stmt = select(ProductModel)
            result = db.execute(stmt)
            return result.scalars().all()
        

    @staticmethod
    def add_product(db: Session,product: ProductSchema) -> ProductModel:
            new_product = ProductModel(
                title=product.title,
                description=product.description,
                price=product.price,
                quantity=product.quantity,
            )

            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            return new_product

    @staticmethod
    def update_product(db: Session,title: str, product: dict[str,Any]) -> bool:
            stmt = (
                update(ProductModel)
                .where(ProductModel.title == title)
                .values(**product)
            )
            result = db.execute(stmt)
            db.commit()
            stmt_select = select(ProductModel).where(ProductModel.title == product.get('title', title))
            updated_product = db.execute(stmt_select).scalar_one_or_none()
            return updated_product 
    

    @staticmethod
    def delete_product(db: Session,title: str) -> bool:
            stmt = delete(ProductModel).where(ProductModel.title == title)
            db.execute(stmt)
            db.commit()
            return True


    @staticmethod
    def get_products_paginated(
        db: Session,
        offset: int = 0, 
        limit: int = 10
    ) -> list[ProductModel]:
            stmt = select(ProductModel).offset(offset).limit(limit)
            result = db.execute(stmt)
            return result.scalars().all()
        

    @staticmethod
    def update_quantity(db: Session,product_id: int,delta: int) -> bool:
            stmt = update(ProductModel).where(
                ProductModel.id == product_id,
            ).values(quantity=ProductModel.quantity + delta)
            result = db.execute(stmt)
            db.commit()
            return result.rowcount > 0
        

    @staticmethod
    def get_total_products_count(db: Session,) -> int:
            stmt = select(func.count(ProductModel.id))
            result = db.execute(stmt)
            return result.scalar()
        
    
