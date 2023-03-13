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

當啟動專案後，會生成新的Item資料表，以及與User表之間建立關係
# SQL User表
create table users
(
    id              int auto_increment
        primary key,
    email           varchar(32) null,
    hashed_password varchar(32) null,
    is_active       tinyint(1)  null,
    constraint ix_users_email
        unique (email)
);

create index ix_users_id
    on users (id);

# Item表
create table items
(
    id          int auto_increment
        primary key,
    title       varchar(32) null,
    description varchar(32) null,
    owner_id    int         null,
    constraint items_ibfk_1
        foreign key (owner_id) references users (id)
);

create index ix_items_description
    on items (description);

create index ix_items_id
    on items (id);

create index ix_items_title
    on items (title);

create index owner_id
    on items (owner_id);
'''

from typing import List
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

# 讀取使用者擁有的item
@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    items = crud.get_item(db=db, skip=skip, limit=limit)
    return items


# 建立使用者的item
@app.post("/users/{user_id}/items", response_model=schemas.Item)
def create_item_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
