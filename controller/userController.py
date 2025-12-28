from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from crud import userCRUD
from schemas.user_schema import LoginRequest, LoginResponse, UserCreate, UserUpdate
from db.models import User
from setting import utils

def map_user_response(user):
    return {
        "id": user.id,
        "username": user.username,
        "roles": [role.name for role in user.roles]
    }

def login(data: LoginRequest, db: Session):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not user.verify_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token_data = {"user_id": str(user.id), "password": user.password}
    access_token = utils.create_access_token(token_data)
    refresh_token = utils.create_refresh_token(token_data)

    return LoginResponse(access_token=access_token, refresh_token=refresh_token)

def createUser(data, db: Session):
    newUser = userCRUD.create_user(db, data)
    if newUser is None:
        raise HTTPException(status_code=400, detail="User already exist")
    
    return map_user_response(newUser)

def getAllUsers(current_user, offset_limit, text_search=None):
    api = userCRUD.DatabaseAPI(current_user)
    offset, limit = offset_limit
    data, total = api.get_all_users(offset, limit, text_search)
    if not data:
        raise HTTPException(status_code=404, detail="List user is empty")
    
    data = data, total
    return utils.get_pages_records(data, offset_limit)

def getInfoById(id: str, current_user):
    api = userCRUD.DatabaseAPI(current_user)
    userInfo = api.get_info_by_id(id)
    if userInfo is None:
        raise HTTPException(status_code=404, detail="User doest not exist")
    
    return map_user_response(userInfo)

def updateUser(data: UserUpdate, current_user):
    api = userCRUD.DatabaseAPI(current_user)
    userUpdate = api.update_user_by_id(data)
    if userUpdate is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return map_user_response(userUpdate)

def deleteUser(id: str, current_user):
    api = userCRUD.DatabaseAPI(current_user)
    success = api.delete_user_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User has been deleted successfully"}
