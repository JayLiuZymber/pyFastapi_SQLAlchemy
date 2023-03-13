# crud.py
'''
資料庫操作相關
通過傳入資料庫連線以及引數等進行資料庫操作，
包括建立使用者、查詢使用者等，返回的是orm模型物件
'''

from sqlalchemy.orm import Session
import models, schemas

# 通過id查詢使用者
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# 新建使用者
def db_create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()  # 提交儲存到資料庫中
    db.refresh(db_user)  # 重新整理
    return db_user
