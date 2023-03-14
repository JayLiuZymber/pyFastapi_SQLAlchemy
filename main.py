# main.py
'''
主檔案
主檔案進行資料庫初始化、FastAPI例項建立以及處理各種請求
進入到互動文件檢視：
http://127.0.0.1:8000/supps/
http://127.0.0.1:8000/docs->POST Request body
# 請求 Postman->POST body raw JSON->SEND
{
    "taxid": "22099131",
    "name": "台灣積體電路製造股份有限公司"
}
# 響應
{
    "taxid": 22099131,
    "name": "台灣積體電路製造股份有限公司",
    "products": []
}

http://127.0.0.1:8000/supp/22099131
# 響應 Postman->GET
{
    "taxid": 22099131,
    "name": "台灣積體電路製造股份有限公司",
    "products": []
}

http://127.0.0.1:8000/supp/22099131/prod
# 請求 POST
{
  "port_number": "1001001",
  "name": "Wifi IC"
}
# 響應
{
    "id": 1,
    "supplier_taxid": 22099131,
    "port_number": 1001001,
    "name": "Wifi IC"
}

http://127.0.0.1:8000/custs/
# 請求 POST = 響應
{
    "taxid": "00000022",
    "name": "泰煜建材股份有限公司"
}

當啟動專案後，會生成新的Item資料表，以及與User表之間建立關係
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

# 首頁
@app.get("/")
def read_root():
    return {"歡迎使用": "進銷存管理系統"}

# 新建供應商
@app.post("/supps/", response_model=schemas.Supplier)
def create_supp(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    return crud.db_create_supp(db=db, supp=supplier)

@app.get("/supp/{supp_taxid}", response_model=schemas.Supplier)
def read_supp(supp_taxid: int, db: Session = Depends(get_db)):
    db_supp = crud.get_supp(db, supp_taxid=supp_taxid)
    if not db_supp:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supp

# 讀取供應商擁有的product
@app.get("/prods/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    products = crud.get_product(db=db, skip=skip, limit=limit)
    return products

# 建立供應商的product
@app.post("/supp/{supp_taxid}/prod", response_model=schemas.Product)
def create_product_supp(supp_taxid: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.db_create_supp_product(db=db, product=product, supp_taxid=supp_taxid)

# -----------------------------------------------------------------------------
# 新建客戶
@app.post("/custs/", response_model=schemas.Customer)
def create_cust(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.db_create_cust(db=db, cust=customer)

@app.get("/cust/{cust_taxid}", response_model=schemas.Customer)
def read_cust(cust_taxid: int, db: Session = Depends(get_db)):
    db_cust = crud.get_cust(db, cust_taxid=cust_taxid)
    if not db_cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_cust
"""
# -----------------------------------------------------------------------------
# 新建使用者
@ app.post("/users/", response_model=schemas.User)
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
 """
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
