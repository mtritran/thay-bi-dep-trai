from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate, UserResponse, LoginResponse, LoginRequest, UserUpdate, PaginatedUserResponse
from db.database import get_db
from controller import userController
from setting.utils import get_current_user, get_offset_limit

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return userController.login(data, db)

@router.post("", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return userController.createUser(data, db)

@router.get("", response_model=PaginatedUserResponse)
def get_all_users(
    current_user = Depends(get_current_user),
    offset_limit = Depends(get_offset_limit),
    text_search: str= None
):
    return userController.getAllUsers(
        current_user = current_user,
        offset_limit = offset_limit,
        text_search = text_search
    )

@router.get("/info", response_model=UserResponse)
def get_info_by_id(id: str, user_context = Depends(get_current_user)):
    return userController.getInfoById(id, user_context)

@router.put("", response_model=UserResponse)
def update_user_by_id(data: UserUpdate, user_context = Depends(get_current_user)):
    return userController.updateUser(data, user_context)

@router.delete("")
def delete_user(id: str, user_context = Depends(get_current_user)):
    return userController.deleteUser(id, user_context)