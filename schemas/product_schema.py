from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class IDN(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None

class CateCreate(BaseModel):
    name: str=None

class ProductDTO(BaseModel):
    id: Optional[UUID] = None
    code: str
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category:IDN

class PaginatedProduct(BaseModel):
    total_pages: int
    total_elements: int
    has_next: bool
    data: list[ProductDTO]

class PaginatedCategory(BaseModel):
    total_pages: int
    total_elements: int
    has_next: bool
    data: list[IDN]