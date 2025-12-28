from fastapi import APIRouter, Depends
from schemas.product_schema import ProductDTO, PaginatedProduct
from controller.product_controller import controller_create_product, controller_get_all_products, controller_get_product_by_code, controller_update_product_by_code, controller_delete_product
from setting.utils import get_current_user, get_offset_limit

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("", response_model=ProductDTO)
def create_product(product_data: ProductDTO, context = Depends(get_current_user)):
    return controller_create_product(context, product_data)

@router.get("", response_model=PaginatedProduct)
def get_all_products(context = Depends(get_current_user), text_search: str = None, offset_limit = Depends(get_offset_limit)):
    return controller_get_all_products(context, text_search, offset_limit)

@router.get("/getByCode", response_model=ProductDTO)
def get_product_by_code(context = Depends(get_current_user), code: str = None):
    return controller_get_product_by_code(context, code)

@router.put("", response_model=ProductDTO)
def update_product_by_code(data: ProductDTO, context = Depends(get_current_user)):
    return controller_update_product_by_code(context, data)

@router.delete("")
def delete_product_by_code(code: str = None, context = Depends(get_current_user)):
    return controller_delete_product(context, code)