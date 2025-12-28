from sqlalchemy.orm import Session
from db.models import User, Role
from setting.config import Settings
from db.role_enums import RoleName

def create_default_admin(db: Session):
    admin_role = db.query(Role).filter(Role.name == RoleName.ADMIN.value).first()

    if not admin_role:
        admin_role = Role(
            name = RoleName.ADMIN.value,
            description="System administrator"
        )

        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    default_admin = db.query(User).filter(User.username == "admin").first()

    if default_admin:
        print(f"Verified: Admin exists with ID {default_admin.id}")

        if admin_role not in default_admin.roles:
            default_admin.roles.append(admin_role)
            db.commit()
        return
    else:
        default_admin = User(
            username = "admin"
        )

        default_admin.set_password(Settings.ADMIN_DEFAULT_PASSWORD)
        default_admin.roles.append(admin_role)

        db.add(default_admin)
        db.commit()
        db.refresh(default_admin)

        print("Default admin account has been created")

def create_user(db: Session, user_in):
    default_role = db.query(Role).filter(Role.name == RoleName.USER.value).first()

    if not default_role:
        default_role = Role(
            name = RoleName.USER.value,
            description="User role"
        )

        db.add(default_role)
        db.commit()
        db.refresh(default_role)

    new_user = db.query(User).filter(User.username == user_in.username).first()

    if new_user:
        if default_role not in new_user.roles:
            new_user.roles.append(default_role)
            db.commit()

        return None

    new_user = User(
        username = user_in.username
    )

    new_user.set_password(user_in.password)
    new_user.roles.append(default_role)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

class DatabaseAPI:
    def __init__(self, current_user):
        db, token_data, _ = current_user
        self.db: Session = db
        self.user_info = token_data

    def get_all_users(self,
                    offset: int = None,
                    limit: int = None,
                    text_search: str = None):
        
        data = self.db.query(User)
        
        if text_search is not None:
            data = data.filter(User.username.ilike(f"%{text_search.lower()}%"))
        total = data.count()
        
        if offset != None and limit != None:
            data = data.offset(offset).limit(limit)

        data = data.all()
        
        rcData = list()
        for record in data:
            item = {
                "id": str(record.id),
                "username": record.username,
                "roles": [role.name for role in record.roles]
            }
            rcData.append(item)

        return rcData, total
    
    def get_info_by_id(self, id: str):
        userInfo = self.db.query(User).filter(User.id == id).first()
        if not userInfo:
            return None
        
        return userInfo

    def update_user_by_id(self, user_in):
        db = self.db
        db_user = db.query(User).filter(User.id == user_in.id).first()
        
        if not db_user:
            return None
        
        db_user.username = user_in.username

        if user_in.password:
            db_user.set_password(user_in.password)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user

    def delete_user_by_id(self, id: str):
        db = self.db
        db_user = db.query(User).filter(User.id == id).first()

        if not db_user:
            return None
        
        db.delete(db_user)
        db.commit()

        return True