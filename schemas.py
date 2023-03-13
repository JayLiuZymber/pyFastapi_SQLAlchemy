# schemas.py
'''
模型驗證
定義請求引數模型驗證與響應模型驗證的Pydantic模型，
其中響應模型中設定orm_mode=True引數，表示與ORM模型相容，
因為後續中返回的資料庫查詢是orm模型，
通過設定這個引數可以將orm模型通過pydantic模型進行驗證
'''

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    """
    請求模型驗證：
    email:
    password:
    """
    password: str

class User(UserBase):
    """
    響應模型：
    id:
    email:
    is_active
    並且設定orm_mode與之相容
    """
    id: int
    is_active: bool

    class Config:
        orm_mode = True
