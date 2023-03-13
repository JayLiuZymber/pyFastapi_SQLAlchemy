# models.py
'''
資料庫模型表
通過資料庫配置檔案中的基類來建立模型類
'''

from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(32), unique=True, index=True)
    hashed_password = Column(String(32))
    is_active = Column(Boolean, default=True)
