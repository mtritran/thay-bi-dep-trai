from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.models import Product
from setting.config import Settings
from uuid import UUID

class ProductAPI:
    def __init__(self, current_user):
        db, token_data, _ = current_user
        self.db: Session = db
        self.user_info = token_data

    def crud_create_product(
        self,
        code: str,
        name: str,
        description: Optional[str],
        price: float,
        category_id: UUID
    ):
        
        db = self.db

        product = Product(
            code=code.strip(),
            name=name,
            description=description,
            price=price,
            category_id=category_id
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product
    
    def crud_get_all_products(self, offset: int = None, limit: int = None, text_search: str = None):
        data = self.db.query(Product)

        if text_search is not None:
            data = data.filter(Product.name.ilike(f"%{text_search}%"))
        total = data.count()

        if offset != None and limit != None:
            data = data.offset(offset).limit(limit)

        data = data.all()
        
        rcData = list()
        for record in data:
            item = {
                "id": str(record.id),
                "code": record.code,
                "name": record.name,
                "description": record.description,
                "price": record.price,
                "category": { 
                    "id": str(record.category.id), 
                    "name": record.category.name 
                }
            }
            rcData.append(item)

        return rcData, total
        
    def crud_get_product_by_code(self, code: str = None):
        product_searched = self.db.query(Product).filter(Product.code == code).first()

        if not product_searched:
            return None
        
        return product_searched
    
    def crud_update_product_by_code(self, name: str, description: str, price: float, code: str = None, category_id: UUID = None):
        db = self.db

        prod = db.query(Product).filter(Product.code == code).first()

        if not prod:
            return None
        
        prod.name = name
        prod.description = description
        prod.price = price
        prod.category_id = category_id
        
        db.add(prod)
        db.commit()
        db.refresh(prod)

        return prod
    
    def crud_delete_product(self, code: str = None):
        db = self.db
        check_prod = db.query(Product).filter(Product.code == code).first()
        
        if not check_prod:
            return None
        
        db.delete(check_prod)
        db.commit()
        
        return True


        
        

