# main.py
'''
主檔案
主檔案進行資料庫初始化、FastAPI例項建立以及處理各種請求
當啟動專案後，會生成新的Item資料表，以及與User表之間建立關係
'''

from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request
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
async def create_supp(supplier: schemas.SupplierCreate, request: Request, db: Session = Depends(get_db)):
    log.debug('')
    raw_head = request.headers['Content-Type']
    log.debug('%s', raw_head)
    if raw_head != 'application/json':
        raise HTTPException(422, detail="Content-Type is not json")
    num = crud.count_supp(db, supplier.taxid)
    if num != 0:
        raise HTTPException(422, detail="Tax ID exist")
    return crud.create_supp(db, supplier)

def exist_supp(supplier_taxid: int, db: Session = Depends(get_db)):
    num = crud.count_supp(db, supplier_taxid)
    log.debug('num=%d', num)
    if num == 0:
        raise HTTPException(404, detail="Supplier not found")
    else:
        return True

# 通過taxid查詢供應商
@app.get("/supp/{supplier_taxid}", response_model=schemas.Supplier)
def get_supp(supplier_taxid: int, db: Session = Depends(get_db)):
    exist_supp(supplier_taxid, db)
    return crud.read_supp(db, supplier_taxid)

# 修改供應商 回傳Supplier
@app.patch("/supp/{supplier_taxid}", response_model=schemas.Supplier)
# 輸入模型 SupplierCreate
def update_supp(supplier_taxid: int, supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    exist_supp(supplier_taxid, db)
    return crud.update_supp(db, supplier_taxid, supplier)

# 刪除供應商 回傳bool
@app.delete("/supp/{supplier_taxid}", response_model=bool)
def delete_supp(supplier_taxid: int, db: Session = Depends(get_db)):
    exist_supp(supplier_taxid, db)
    return crud.delete_supp(db, supplier_taxid)

# -----------------------------------------------------------------------------
# 建立供應商的產品
@app.post("/supp/{supplier_taxid}/prod", response_model=schemas.Product)
def create_supp_product(supplier_taxid: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    exist_supp(supplier_taxid, db)
    num = crud.count_supp_product(db, product.port_number)
    if num != 0:
        raise HTTPException(422, detail="Port Number exist")
    return crud.create_supp_product(db, supplier_taxid, product)

def exist_supp_product(port_number: int, db: Session = Depends(get_db)):
    num = crud.count_supp_product(db, port_number)
    log.debug('num=%d', num)
    if num == 0:
        raise HTTPException(404, detail="Product not found")
    else:
        return True

# 通過port_number查詢產品
@app.get("/supp/{supplier_taxid}/prod/{port_number}", response_model=schemas.Product)
def get_supp_product(port_number: int, db: Session = Depends(get_db)):
    exist_supp_product(port_number, db)
    return crud.read_supp_product(db, port_number)

# 刪除產品 回傳bool
@app.delete("/supp/{supplier_taxid}/prod/{port_number}", response_model=bool)
def delete_supp_product(port_number: int, db: Session = Depends(get_db)):
    exist_supp_product(port_number, db)
    return crud.delete_supp_product(db, port_number)

# 讀取供應商擁有的產品
@app.get("/supp/{supplier_taxid}/prods", response_model=List[schemas.Product])
def get_supp_products(supplier_taxid: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    exist_supp(supplier_taxid, db)
    return crud.read_supp_all_product(db, skip=skip, limit=limit, supp_taxid=supplier_taxid)

# 讀取所有的product
@app.get("/prods/", response_model=List[schemas.Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_all_product(db, skip=skip, limit=limit)

# -----------------------------------------------------------------------------
# 建立進貨單
@app.post("/pos/", response_model=schemas.PurchaseOrder)
# 輸入模型 PurchaseOrderCreate
def create_supp_order(purchase_order: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    log.debug('')
    db_prod = crud.read_supp_product(db, port_number=purchase_order.product_pn)
    if not db_prod:
        raise HTTPException(404, detail="Product not found")
    exist_supp(db_prod.supplier_taxid, db)
    return crud.create_supp_order(db, order=purchase_order)

def exist_supp_order(order_id: int, db: Session = Depends(get_db)):
    num = crud.count_supp_order(order_id, db)
    log.debug('num=%d', num)
    if num == 0:
        raise HTTPException(404, detail="Purchase Order not found")
    else:
        return True

def exist_supp_order_by_id(id: int, db: Session = Depends(get_db)):
    num = crud.count_supp_order_by_id(db, id=id)
    log.debug('num=%d', num)
    if num == 0:
        raise HTTPException(404, detail="Purchase Order ID not found")
    else:
        return True

# 通過id查詢進貨單
@app.get("/po_id/{id}", response_model=schemas.PurchaseOrder)
def get_supp_order_by_id(id: int, db: Session = Depends(get_db)):
    log.debug('')
    exist_supp_order_by_id(id, db)
    return crud.read_supp_order_by_id(db, id=id)

# 通過id修改進貨單 回傳PurchaseOrder
@app.patch("/po_id/{id}", response_model=schemas.PurchaseOrder)
# 輸入模型 PurchaseOrderCreate
def update_supp_by_id(id: int, order: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    exist_supp_order_by_id(id, db)
    exist_supp_product(order.product_pn, db)
    return crud.update_supp_order_by_id(db, id, order)

# 通過id刪除進貨單
@app.delete("/po_id/{id}", response_model=bool)
def delete_supp_order_by_id(id: int, db: Session = Depends(get_db)):
    log.debug('')
    exist_supp_order_by_id(id, db)
    return crud.delete_supp_order_by_id(db, id)

# 通過order_id查詢進貨單
@app.get("/po/{order_id}", response_model=schemas.PurchaseOrder)
def get_supp_order(order_id: int, db: Session = Depends(get_db)):
    exist_supp_order(order_id, db)
    return crud.read_supp_order(db, order_id)

# 修改進貨單 回傳PurchaseOrder
@app.patch("/po/{order_id}", response_model=schemas.PurchaseOrder)
# 輸入模型 PurchaseOrderCreate
def update_supp(order_id: int, order: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    exist_supp_order(order_id, db)
    exist_supp_product(order.product_pn, db)
    return crud.update_supp_order(db, order_id, order)

# 通過order_id刪除進貨單
@app.delete("/po/{order_id}", response_model=bool)
def delete_supp_order(order_id: int, db: Session = Depends(get_db)):
    exist_supp_order(order_id, db)
    return crud.delete_supp_order(db, order_id)

# -----------------------------------------------------------------------------
# 新建客戶
@app.post("/custs/", response_model=schemas.Customer)
def create_cust(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    num = crud.count_cust(db, customer.taxid)
    if num != 0:
        raise HTTPException(422, detail="Tax ID exist")
    return crud.create_cust(db, cust=customer)

def exist_cust(customer_taxid: int, db: Session = Depends(get_db)):
    num = crud.count_cust(db, customer_taxid)
    log.debug('num=%d', num)
    if num == 0:
        raise HTTPException(404, detail="Customer not found")
    else:
        return True

# 通過taxid查詢客戶
@app.get("/cust/{customer_taxid}", response_model=schemas.Customer)
def get_cust(customer_taxid: int, db: Session = Depends(get_db)):
    exist_cust(customer_taxid, db)
    return crud.read_cust(db, cust_taxid=customer_taxid)

# 修改客戶 回傳Customer
@app.patch("/cust/{customer_taxid}", response_model=schemas.Customer)
# 輸入模型 CustomerCreate
def update_supp(customer_taxid: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    exist_cust(customer_taxid, db)
    return crud.update_cust(db, cust_taxid=customer_taxid, cust=customer)

# 刪除客戶
@app.delete("/cust/{customer_taxid}", response_model=bool)
def delete_cust(customer_taxid: int, db: Session = Depends(get_db)):
    exist_cust(customer_taxid, db)
    return crud.delete_cust(db, cust_taxid=customer_taxid)

# -----------------------------------------------------------------------------
# 建立出貨單
@app.post("/sos/", response_model=schemas.SellOrder)
# 輸入模型 SellOrderCreate
def create_cust_order(purchase_order: schemas.SellOrderCreate, db: Session = Depends(get_db)):
    log.debug('')
    exist_supp_product(purchase_order.product_pn, db)
    exist_cust(purchase_order.customer_taxid, db)
    try:
        return crud.create_cust_order(db, order=purchase_order)
    except Exception as e:
        log.error(e)
        raise HTTPException(422, detail="Create Sell Order error")

def exist_cust_order(order_id: int, db: Session = Depends(get_db)):
    num = crud.count_cust_order(order_id, db)
    log.debug('num=%d', num)
    if num == 0:
        raise HTTPException(404, detail="Sell Order not found")
    else:
        return True

def exist_cust_order_by_id(id: int, db: Session = Depends(get_db)):
    num = crud.count_cust_order_by_id(db, id)
    log.debug('num=%d', num)
    if num == 0:
        raise HTTPException(404, detail="Sell Order ID not found")
    else:
        return True

# 通過id查詢出貨單
@app.get("/so_id/{id}", response_model=schemas.SellOrder)
def get_cust_order_by_id(id: int, db: Session = Depends(get_db)):
    log.debug('')
    exist_cust_order_by_id(id, db)
    return crud.read_cust_order_by_id(db, id)

# 通過id修改出貨單 回傳SellOrder
@app.patch("/so_id/{id}", response_model=schemas.SellOrder)
# 輸入模型 SellOrderCreate
def update_cust_by_id(id: int, order: schemas.SellOrderCreate, db: Session = Depends(get_db)):
    exist_cust_order_by_id(id, db)
    exist_supp_product(order.product_pn, db)
    exist_cust(order.customer_taxid, db)
    try:
        return crud.update_cust_order_by_id(db, id, order)
    except Exception as e:
        log.error(e)
        raise HTTPException(422, detail="Update Sell Order error")

# 通過id刪除出貨單
@app.delete("/so_id/{id}", response_model=bool)
def delete_cust_order_by_id(id: int, db: Session = Depends(get_db)):
    log.debug('')
    exist_cust_order_by_id(id, db)
    return crud.delete_cust_order_by_id(db, id)

# 通過order_id查詢出貨單
@app.get("/so/{order_id}", response_model=schemas.SellOrder)
def get_cust_order(order_id: int, db: Session = Depends(get_db)):
    exist_cust_order(order_id, db)
    return crud.read_cust_order(db, order_id)

# 修改出貨單 回傳SellOrder
@app.patch("/so/{order_id}", response_model=schemas.SellOrder)
# 輸入模型 SellOrderCreate
def update_supp(order_id: int, order: schemas.SellOrderCreate, db: Session = Depends(get_db)):
    exist_cust_order(order_id, db)
    exist_supp_product(order.product_pn, db)
    exist_cust(order.customer_taxid, db)
    try:
        return crud.update_cust_order(db, order_id, order)
    except Exception as e:
        log.error(e)
        raise HTTPException(422, detail="Update Sell Order error")

# 通過order_id刪除出貨單
@app.delete("/so/{order_id}", response_model=bool)
def delete_cust_order(order_id: int, db: Session = Depends(get_db)):
    exist_cust_order(order_id, db)
    return crud.delete_cust_order(db, order_id)

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
