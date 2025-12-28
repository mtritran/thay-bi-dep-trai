from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from crud import product_crud
from schemas.product_schema import ProductDTO
from db.models import Product, Category
from fastapi import HTTPException, status

from setting.utils import get_pages_records

def controller_create_product(context, product_data: ProductDTO):
    if not product_data.code or not product_data.code.strip():
        raise ValueError("Product code cannot be empty")
    
    if not product_data.name or not product_data.name.strip():
        raise ValueError("Product name cannot be empty")

    if not product_data.price:
        raise ValueError("Product price cannot be empty")
    
    if not product_data.category.id:
        raise ValueError("Category id cannot be empty")

    api = product_crud.ProductAPI(context)
    db = api.db

    existedCate = db.query(Category).filter(Category.id == product_data.category.id).first()

    if not existedCate:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "This category does not existed")
    
    existed_code = db.query(Product).filter(Product.code == product_data.code).first()
    if existed_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product code already exists"
        )

    existed = (
        db.query(Product)
        .filter(Product.name == product_data.name)
        .first()
    )

    if existed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This product already exists"
        )

    return api.crud_create_product(
        code=product_data.code,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        category_id=product_data.category.id
    )

def controller_get_all_products(context, text_search, offset_limit):
    api = product_crud.ProductAPI(context)
    offset, limit = offset_limit
    data, total = api.crud_get_all_products(offset,limit,text_search)
    if not data:
        raise HTTPException(status_code=404, detail="No products found")
    data=data, total
    return get_pages_records(data,offset_limit)

def controller_get_product_by_code(context, code: str = None):
    api = product_crud.ProductAPI(context)

    product_searched = api.crud_get_product_by_code(code)

    if product_searched is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found")
    
    return product_searched

def controller_update_product_by_code(context, product_data: ProductDTO):
    if not product_data.code or not product_data.code.strip():
        raise ValueError("Product code cannot be empty")
    
    api = product_crud.ProductAPI(context)

    existedCate = api.db.query(Category).filter(Category.id == product_data.category.id).first()

    if not existedCate:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "This category does not existed")

    product_update = api.crud_update_product_by_code(product_data.name, product_data.description, product_data.price, product_data.code, product_data.category.id)

    if product_update is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found")
    
    return product_update

def controller_delete_product(context, code: str = None):
    api = product_crud.ProductAPI(context)

    delete_prod = api.crud_delete_product(code)

    if delete_prod is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found")
    
    if delete_prod:
        return "This product has been deleted"
