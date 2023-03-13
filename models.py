# models.py
'''
資料庫模型表
通過資料庫配置檔案中的基類來建立模型類
複雜例項 在之前的基礎上再加一個模型類Item，User與之是一對多的關係
'''

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(32), unique=True, index=True)
    hashed_password = Column(String(32))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(32), index=True)
    description = Column(String(32), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
    