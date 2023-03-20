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

http://127.0.0.1:8000/pos
# 請求 POST
{
    "product_pn": 1001001,
    "cost_price": 200,
    "amount": 33
}
# 響應
{
    "cost_price": 200,
    "amount": 33,
    "id": 3,
    "time": "2023-03-20T11:22:29",
    "order_id": 20230311.2229,
    "supplier_taxid": 22099131,
    "supplier_name": "台灣積體電路製造股份有限公司",
    "product_pn": 1001001,
    "product_id": 3,
    "product_name": "Wifi IC",
    "total_price": 6600
}
# 請求 Postman->PATCH = 請求
{
    "product_pn": 1001001,
    "cost_price": 300,
    "amount": 44
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
import logs

Base.metadata.create_all(bind=engine) #資料庫初始化，如果沒有庫或者表，會自動建立

app = FastAPI()
log = logs.getLogger(__name__, logs.DEBUG, True)
log.info('log start ...')

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
def get_root():
    log.debug('')
    return {"歡迎使用": "進銷存管理系統"}

# -----------------------------------------------------------------------------
# 新建供應商
@app.post("/supps/", response_model=schemas.Supplier)
def create_supp(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    return crud.db_create_supp(db=db, supp=supplier)

def exist_supp(supplier_taxid: int, db: Session = Depends(get_db)):
    num = crud.count_supp(db, supp_taxid=supplier_taxid)
    log.debug('num=%d', num)
    if num == 0:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return True

# 通過taxid查詢供應商
@app.get("/supp/{supplier_taxid}", response_model=schemas.Supplier)
def get_supp(supplier_taxid: int, db: Session = Depends(get_db)):
    exist_supp(supplier_taxid=supplier_taxid, db=db)
    return crud.db_read_supp(db, supp_taxid=supplier_taxid)

# 修改供應商 回傳Supplier
@app.patch("/supp/{supplier_taxid}", response_model=schemas.Supplier)
# 輸入模型 SupplierCreate
def update_supp(supplier_taxid: int, supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    exist_supp(supplier_taxid=supplier_taxid, db=db) 
    return crud.db_update_supp(db, supp_taxid=supplier_taxid, supp=supplier)

# 刪除供應商 回傳bool
@app.delete("/supp/{supplier_taxid}", response_model=bool)
def delete_supp(supplier_taxid: int, db: Session = Depends(get_db)):
    exist_supp(supplier_taxid=supplier_taxid, db=db)
    return crud.db_delete_supp(db, supp_taxid=supplier_taxid)

# -----------------------------------------------------------------------------
# 建立供應商的產品
@app.post("/supp/{supplier_taxid}/prod", response_model=schemas.Product)
def create_supp_product(supplier_taxid: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.db_create_supp_product(db=db, prod=product, supp_taxid=supplier_taxid)

# 通過port_number查詢產品
@app.get("/supp/{supplier_taxid}/prod/{port_number}", response_model=schemas.Product)
def get_supp_product(port_number: int, db: Session = Depends(get_db)):
    return crud.db_read_supp_product(db=db, port_number=port_number)

# 刪除產品 回傳bool
@app.delete("/supp/{supplier_taxid}/prod/{port_number}", response_model=bool)
def delete_supp_product(port_number: int, db: Session = Depends(get_db)):
    db_prod = crud.db_read_supp_product(db, port_number=port_number)
    if not db_prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.db_delete_supp_product(db, port_number=port_number)

# 讀取供應商擁有的產品
@app.get("/supp/{supplier_taxid}/prods", response_model=List[schemas.Product])
def get_supp_products(supplier_taxid: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prods = crud.db_read_supp_all_product(db=db, skip=skip, limit=limit, supp_taxid=supplier_taxid)
    return prods

# 讀取所有的product
@app.get("/prods/", response_model=List[schemas.Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prods = crud.db_read_all_product(db=db, skip=skip, limit=limit)
    return prods

# -----------------------------------------------------------------------------
# 建立進貨單
@app.post("/pos/", response_model=schemas.PurchaseOrder)
# 輸入模型 PurchaseOrderCreate
def create_porder(purchase_order: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    log.debug('')
    db_prod = crud.db_read_supp_product(db=db, port_number=purchase_order.product_pn)
    if not db_prod:
        raise HTTPException(status_code=404, detail="Product not found")
    exist_supp(supplier_taxid=db_prod.supplier_taxid, db=db)
    return crud.db_create_supp_order(db=db, order=purchase_order)
    
def exist_supp_order(order_id: int, db: Session = Depends(get_db)):
    num = crud.count_supp_order(order_id=order_id, db=db)
    log.debug('num=%d', num)
    if num == 0:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    else:
        return True
  
def exist_supp_order_by_id(id: int, db: Session = Depends(get_db)):
    num = crud.count_supp_order_by_id(db=db, id=id)
    log.debug('num=%d', num)
    if num == 0:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    else:
        return True
  
# 通過id查詢進貨單
@app.get("/po_id/{id}", response_model=schemas.PurchaseOrder)
def get_supp_order_by_id(id: int, db: Session = Depends(get_db)):
    log.debug('')
    exist_supp_order_by_id(id=id, db=db)
    return crud.db_read_supp_order_by_id(db=db, id=id)

# 通過id修改進貨單 回傳PurchaseOrder
@app.patch("/po_id/{id}", response_model=schemas.PurchaseOrder)
# 輸入模型 PurchaseOrderCreate
def update_supp_by_id(id: int, order: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    exist_supp_order_by_id(id=id, db=db)
    return crud.db_update_supp_order_by_id(db=db, id=id, order=order)

# 通過id刪除進貨單
@app.delete("/po_id/{id}", response_model=bool)
def delete_supp_order_by_id(id: int, db: Session = Depends(get_db)):
    log.debug('')
    exist_supp_order_by_id(id=id, db=db)
    return crud.db_delete_supp_order_by_id(db=db, id=id)

# 通過order_id查詢進貨單
@app.get("/po/{order_id}", response_model=schemas.PurchaseOrder)
def get_supp_order(order_id: int, db: Session = Depends(get_db)):
    exist_supp_order(order_id=order_id, db=db)
    return crud.db_read_supp_order(db=db, order_id=order_id)

# 修改進貨單 回傳PurchaseOrder
@app.patch("/po/{order_id}", response_model=schemas.PurchaseOrder)
# 輸入模型 PurchaseOrderCreate
def update_supp(order_id: int, order: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    exist_supp_order(order_id=order_id, db=db)
    return crud.db_update_supp_order(db=db, order_id=order_id, order=order)

# 通過order_id刪除進貨單
@app.delete("/po/{order_id}", response_model=bool)
def delete_supp_order(order_id: int, db: Session = Depends(get_db)):
    exist_supp_order(order_id=order_id, db=db)
    return crud.db_delete_supp_order(db=db, order_id=order_id)

# -----------------------------------------------------------------------------
# 新建客戶
@app.post("/custs/", response_model=schemas.Customer)
def create_cust(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.db_create_cust(db, cust=customer)

def exist_cust(customer_taxid: int, db: Session = Depends(get_db)):
    num = crud.count_cust(db, cust_taxid=customer_taxid)
    if num == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return True

# 通過taxid查詢客戶
@app.get("/cust/{customer_taxid}", response_model=schemas.Customer)
def get_cust(customer_taxid: int, db: Session = Depends(get_db)):
    exist_cust(customer_taxid=customer_taxid, db=db)
    return crud.db_read_cust(db, cust_taxid=customer_taxid)

# 修改客戶 回傳Customer
@app.patch("/cust/{customer_taxid}", response_model=schemas.Customer)
# 輸入模型 CustomerCreate
def update_supp(customer_taxid: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    exist_cust(customer_taxid=customer_taxid, db=db)
    return crud.db_update_cust(db, cust_taxid=customer_taxid, cust=customer)

# 刪除客戶
@app.delete("/cust/{customer_taxid}", response_model=bool)
def delete_cust(customer_taxid: int, db: Session = Depends(get_db)):
    exist_cust(customer_taxid=customer_taxid, db=db)
    return crud.db_delete_cust(db, cust_taxid=customer_taxid)

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
