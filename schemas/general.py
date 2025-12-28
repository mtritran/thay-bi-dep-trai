from pydantic import BaseModel
from typing import Optional

# Tương đương với một LookupDTO trong Java
class ID_NAME(BaseModel):
    """
    Dùng cho các trường hợp chỉ cần trả về ID và Tên.
    Ví dụ: Danh sách các vai trò (Role) để chọn trong Dropdown.
    """
    id: Optional[int] = None
    name: Optional[str] = None

# Tương đương với PageResponse trong Spring Data JPA
class ListGeneral(BaseModel):
    """
    Cấu trúc chuẩn để trả về dữ liệu dạng danh sách có phân trang.
    Giúp Frontend biết khi nào cần hiển thị nút 'Trang tiếp theo'.
    """
    total_pages: int      # Tổng số trang
    total_elements: int   # Tổng số bản ghi trong DB
    has_next: bool        # Có trang tiếp theo hay không?