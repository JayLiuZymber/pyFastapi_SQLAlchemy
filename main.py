# main.py
'''
主檔案
主檔案進行資料庫初始化、FastAPI例項建立以及處理各種請求
進入到互動文件檢視：
http://127.0.0.1:8000/users/
http://127.0.0.1:8000/docs POST Request body
# 請求
{
  "email": "hhh@example113.com",
  "password": "ss123456"
}

# 響應
{
  "email": "hhh@example113.com",
  "id": 7,
  "is_active": true
}

http://127.0.0.1:8000/user/7
# 響應
{
  "email": "hhh@example113.com",
  "id": 7,
  "is_active": true
}
'''

from fastapi import FastAPI, Depends, HTTPException
import crud, schemas
from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
import uvicorn

Base.metadata.create_all(bind=engine) #資料庫初始化，如果沒有庫或者表，會自動建立

app = FastAPI()

# Dependency
def get_db():
    """
    每一個請求處理完畢後會關閉當前連線，不同的請求使用不同的連線
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 新建使用者
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.db_create_user(db=db, user=user)

# 通過id查詢使用者
@app.get("/user/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
