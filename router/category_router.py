from fastapi import APIRouter, Depends
from schemas.product_schema import IDN, PaginatedCategory, CateCreate
from setting.utils import get_current_user, get_offset_limit
from controller.category_controller import controller_create_category, controller_get_all_categories, controller_get_category_by_id, controller_update_category_by_id, controller_delete_category

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("", response_model=IDN)
def create_category(cate_data: CateCreate, context = Depends(get_current_user)):
    return controller_create_category(context, cate_data)

@router.get("", response_model=PaginatedCategory)
def get_all_categories(context = Depends(get_current_user), text_search: str = None, offset_limit = Depends(get_offset_limit)):
    return controller_get_all_categories(context, text_search, offset_limit)

@router.get("/getByCode", response_model=IDN)
def get_category_by_id(context = Depends(get_current_user), id: str = None):
    return controller_get_category_by_id(context, id)

@router.put("", response_model=IDN)
def update_category_by_id(data: IDN, context = Depends(get_current_user)):
    return controller_update_category_by_id(context, data)

@router.delete("")
def delete_category_by_id(id: str = None, context = Depends(get_current_user)):
    return controller_delete_category(context, id)