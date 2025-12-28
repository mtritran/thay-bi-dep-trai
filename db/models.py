import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID  
from sqlalchemy import Column, Float, ForeignKey, String, Table
from sqlalchemy.orm import relationship
from db.database import Base 
from passlib.hash import bcrypt 

MAX_BCRYPT_LENGTH = 72 

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', UUID(as_uuid=True), ForeignKey('role.id', ondelete='CASCADE'), primary_key=True)
)

from sqlalchemy import (
    Column, String
)

class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        index=True
    )
    
    username = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    roles = relationship("Role", secondary=user_roles, back_populates="users")

    def verify_password(self, password: str) -> bool:
        truncated_password = password.encode('utf-8')[:MAX_BCRYPT_LENGTH]
        return bcrypt.verify(truncated_password, self.password)

    def set_password(self, password: str):
        truncated_password = password.encode('utf-8')[:MAX_BCRYPT_LENGTH]
        self.password = bcrypt.hash(truncated_password)

class Role(Base):
    __tablename__ = "role"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255))
        
    users = relationship("User", secondary=user_roles, back_populates="roles")

class Category(Base):
    __tablename__ = "category"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "product"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)

    category_id = Column(UUID(as_uuid=True), ForeignKey("category.id"), nullable=False)

    category = relationship("Category", back_populates="products")



