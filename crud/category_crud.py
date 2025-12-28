from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.models import Category
from setting.config import Settings

class CategoryAPI:
    def __init__(self, current_user):
        db, token_data, _ = current_user
        self.db: Session = db
        self.user_info = token_data

    def crud_create_category(
        self,
        name: str
    ):
        
        db = self.db

        category = Category(
            name = name
        )

        db.add(category)
        db.commit()
        db.refresh(category)

        return category
    
    def crud_get_all_categories(self, offset: int = None, limit: int = None, text_search: str = None):
        data = self.db.query(Category)

        if text_search is not None:
            data = data.filter(Category.name.ilike(f"%{text_search}%"))
        total = data.count()

        if offset != None and limit != None:
            data = data.offset(offset).limit(limit)

        data = data.all()
        
        rcData = list()
        for record in data:
            item = {
                "id": str(record.id),
                "name": record.name
            }
            rcData.append(item)

        return rcData, total
        
    def crud_get_category_by_id(self, id: str = None):
        category_searched = self.db.query(Category).filter(Category.id == id).first()

        if not category_searched:
            return None
        
        return category_searched
    
    def crud_update_category_by_id(self, name: str, id: str = None):
        db = self.db

        cate = db.query(Category).filter(Category.id == id).first()

        if not cate:
            return None
        
        cate.name = name
        
        db.add(cate)
        db.commit()
        db.refresh(cate)

        return cate
    
    def crud_delete_category(self, id: str = None):
        db = self.db
        check_cate = db.query(Category).filter(Category.id == id).first()
        
        if not check_cate:
            return None
        
        db.delete(check_cate)
        db.commit()
        
        return True


        
        

