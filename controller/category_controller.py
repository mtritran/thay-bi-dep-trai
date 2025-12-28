from fastapi import HTTPException, Depends, status
from crud import category_crud
from schemas.product_schema import CateCreate, IDN
from db.models import Category
from fastapi import HTTPException, status

from setting.utils import get_pages_records

def controller_create_category(context, category_data: CateCreate):
    if not category_data.name or category_data.name.strip() == "":
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail = "Category name cannot be empty"
        )

    api = category_crud.CategoryAPI(context)
    db = api.db

    existed = (
        db.query(Category)
        .filter(Category.name == category_data.name)
        .first()
    )

    if existed:
        raise HTTPException(
            status = status.HTTP_400_BAD_REQUEST,
            detail = "This category already exists"
        )

    return api.crud_create_category(
        name = category_data.name
    )

def controller_get_all_categories(context, text_search, offset_limit):
    api = category_crud.CategoryAPI(context)
    offset, limit = offset_limit
    data, total = api.crud_get_all_categories(offset,limit,text_search)
    if not data:
        raise HTTPException(status_code=404, detail="No category found")
    data=data, total
    return get_pages_records(data,offset_limit)

def controller_get_category_by_id(context, id: str = None):
    api = category_crud.CategoryAPI(context)

    cate_searched = api.crud_get_category_by_id(id)

    if cate_searched is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Category not found")
    
    return cate_searched

def controller_update_category_by_id(context, data: IDN):
    api = category_crud.CategoryAPI(context)

    cate_update = api.crud_update_category_by_id(data.name, data.id)

    if cate_update is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Category not found")
    
    return cate_update

def controller_delete_category(context, id: str = None):
    api = category_crud.CategoryAPI(context)

    delete_cate = api.crud_delete_category(id)

    if delete_cate is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Category not found")
    
    if delete_cate:
        return "This category has been deleted"
