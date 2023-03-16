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
# 請求 Postman->PATCH = 請求
{
    "taxid": "22099131",
    "name": "台灣積體電路製造股份有限公司II"
}
# 響應 Postman->DELETE
true

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

http://127.0.0.1:8000/supp/22099131/prod/1001001
# 響應 GET
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

# -----------------------------------------------------------------------------
# 新建供應商
@app.post("/supps/", response_model=schemas.Supplier)
def create_supp(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    return crud.db_create_supp(db=db, supp=supplier)

# 刪除供應商 回傳bool
@app.delete("/supp/{supplier_taxid}", response_model=bool)
def delete_supp(supplier_taxid: int, db: Session = Depends(get_db)):
    db_supp = crud.db_get_supp(db, supp_taxid=supplier_taxid)
    if not db_supp:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return crud.db_delete_supp(db, supp_taxid=supplier_taxid)

# 通過taxid查詢供應商
@app.get("/supp/{supplier_taxid}", response_model=schemas.Supplier)
def read_supp(supplier_taxid: int, db: Session = Depends(get_db)):
    db_supp = crud.db_get_supp(db, supp_taxid=supplier_taxid)
    if not db_supp:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supp

# 修改供應商 回傳Supplier
@app.patch("/supp/{supplier_taxid}", response_model=schemas.Supplier)
# 輸入模型 SupplierCreate
def update_supp(supplier_taxid: int, supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    db_supp = crud.db_get_supp(db, supp_taxid=supplier_taxid)
    if not db_supp:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db_supp = crud.db_set_supp(db, supp_taxid=supplier_taxid, supp=supplier)
    return db_supp

# -----------------------------------------------------------------------------
# 建立供應商的產品
@app.post("/supp/{supplier_taxid}/prod", response_model=schemas.Product)
def create_supp_product(supplier_taxid: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.db_create_supp_product(db=db, prod=product, supp_taxid=supplier_taxid)

# 通過port_number查詢產品
@app.get("/supp/{supplier_taxid}/prod/{port_number}", response_model=schemas.Product)
def get_supp_product(port_number: int, db: Session = Depends(get_db)):
    return crud.db_get_supp_product(db=db, port_number=port_number)

# 讀取供應商擁有的產品
@app.get("/supp/{supplier_taxid}/prods", response_model=List[schemas.Product])
def read_supp_products(supplier_taxid: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prods = crud.db_get_supp_all_product(db=db, skip=skip, limit=limit, supp_taxid=supplier_taxid)
    return prods

# 讀取所有的product
@app.get("/prods/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prods = crud.db_get_product(db=db, skip=skip, limit=limit)
    return prods

# -----------------------------------------------------------------------------
# 新建客戶
@app.post("/custs/", response_model=schemas.Customer)
def create_cust(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.db_create_cust(db=db, cust=customer)

# 刪除客戶
@app.delete("/cust/{customer_taxid}", response_model=bool)
def delete_cust(customer_taxid: int, db: Session = Depends(get_db)):
    db_cust = crud.db_get_cust(db, cust_taxid=customer_taxid)
    if not db_cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.db_delete_cust(db, cust_taxid=customer_taxid)

# 通過taxid查詢客戶
@app.get("/cust/{customer_taxid}", response_model=schemas.Customer)
def read_cust(customer_taxid: int, db: Session = Depends(get_db)):
    db_cust = crud.db_get_cust(db, cust_taxid=customer_taxid)
    if not db_cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_cust

# 修改客戶 回傳Customer
@app.patch("/cust/{customer_taxid}", response_model=schemas.Customer)
# 輸入模型 CustomerCreate
def update_supp(customer_taxid: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_cust = crud.db_get_cust(db, cust_taxid=customer_taxid)
    if not db_cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    db_cust = crud.db_set_cust(db, cust_taxid=customer_taxid, cust=customer)
    return db_cust

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
