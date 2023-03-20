# crud.py
'''
資料庫操作相關
通過傳入資料庫連線以及引數等進行資料庫操作，
包括建立使用者、查詢使用者等，返回的是orm模型物件
'''

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import models, schemas
import logs

log = logs.getLogger(__name__, logs.DEBUG, True)
# log.debug('xxx')

# -----------------------------------------------------------------------------
# 新建供應商
def db_create_supp(db: Session, supp: schemas.SupplierCreate):
    db_supp = models.Supplier(  taxid = supp.taxid, name = supp.name)
    db.add(db_supp)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_supp) # 重新整理
    return db_supp

def count_supp(db: Session, supp_taxid: int):
    return db.query(models.Supplier).filter(models.Supplier.taxid == supp_taxid).count()

# 通過taxid查詢供應商
def db_read_supp(db: Session, supp_taxid: int):
    return db.query(models.Supplier).filter(models.Supplier.taxid == supp_taxid).first()

# 修改供應商
def db_update_supp(db: Session, supp_taxid: int, supp: schemas.Supplier):
    db_supp = db.query(models.Supplier).filter(models.Supplier.taxid == supp_taxid).first()
    db_supp.taxid = supp.taxid
    db_supp.name = supp.name
    db.add(db_supp)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_supp) # 重新整理
    return db_supp

# 刪除供應商
def db_delete_supp(db: Session, supp_taxid: int):
    res = db.query(models.Supplier).filter(models.Supplier.taxid == supp_taxid).delete()
    db.commit()
    return res

# -----------------------------------------------------------------------------
# 新建供應商的product
def db_create_supp_product(db: Session, prod: schemas.ProductCreate, supp_taxid: int):
    db_prod = models.Product(**prod.dict(), supplier_taxid = supp_taxid)
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

def count_supp_product(db: Session, port_number: int):
    return db.query(models.Product).filter(models.Product.port_number == port_number).count()

# 通過port_number查詢產品
def db_read_supp_product(db: Session, port_number: int):
    return db.query(models.Product).filter(models.Product.port_number == port_number).first()

# 讀取供應商擁有的product
def db_read_supp_all_product(supp_taxid: int, db: Session, skip: int = 0, limit: int = 100):
    db_prod = db.query(models.Product).filter(models.Product.supplier_taxid == supp_taxid)
    return db_prod.offset(skip).limit(limit).all()

# 獲取所有的product
def db_read_all_product(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

# 刪除產品
def db_delete_supp_product(db: Session, port_number: int):
    res = db.query(models.Product).filter(models.Product.port_number == port_number).delete()
    db.commit()
    return res

# -----------------------------------------------------------------------------
# 新增進貨單
def db_create_supp_order(db: Session, order: schemas.PurchaseOrderCreate):
    log.debug('')
    db_prob = db_read_supp_product(db=db, port_number = order.product_pn)
    db_supp = db_read_supp(db=db, supp_taxid = db_prob.supplier_taxid)
    # db_time = DateTime(timezone=True, server_default=func.now())
    db_order = models.PurchaseOrder( #order_id = db_time.strf,\
                                    supplier_taxid = db_supp.taxid, \
                                    supplier_name = db_supp.name, \
                                    
                                    product_id = db_prob.id, \
                                    product_pn = db_prob.port_number, \
                                    product_name = db_prob.name, \
                                    
                                    cost_price = order.cost_price, \
                                    amount = order.amount, \
                                    total_price = order.cost_price * order.amount )
    db.add(db_order)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_order) # 重新整理
    return db_order

def count_supp_order_by_id(db: Session, id: int):
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == id).count()

# 通過id查詢進貨單
def db_read_supp_order_by_id(db: Session, id: int):
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == id).first()

# 通過id修改客戶
def db_update_supp_order_by_id(db: Session, id: int, order: schemas.PurchaseOrder):
    db_po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == id).first()
    db_po.cost_price = order.cost_price
    db_po.amount = order.amount
    db_po.total_price = order.cost_price * order.amount
    db_po.product_pn = order.product_pn

    db_prob = db_read_supp_product(db=db, port_number = order.product_pn)
    db_po.product_id = db_prob.id
    db_po.product_pn = db_prob.port_number
    db_po.product_name = db_prob.name
    
    db_supp = db_read_supp(db=db, supp_taxid = db_prob.supplier_taxid)
    db_po.supplier_taxid = db_supp.taxid
    db_po.supplier_name = db_supp.name
    db.add(db_po)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_po) # 重新整理
    return db_po

# 通過id刪除進貨單
def db_delete_supp_order_by_id(db: Session, id: int):
    res = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == id).delete()
    db.commit()
    return res

# -----------------------------------------------------------------------------
def count_supp_order(db: Session, order_id: int):
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.order_id == order_id).count()

# 通過order_id查詢進貨單
def db_read_supp_order(db: Session, order_id: int):
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.order_id == order_id).first()

# 通過order_id修改客戶
def db_update_supp_order(db: Session, order_id: int, order: schemas.PurchaseOrder):
    db_po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.order_id == order_id).first()
    db_po.cost_price = order.cost_price
    db_po.amount = order.amount
    db_po.total_price = order.cost_price * order.amount
    db_po.product_pn = order.product_pn

    db_prob = db_read_supp_product(db=db, port_number = order.product_pn)
    db_po.product_id = db_prob.id
    db_po.product_pn = db_prob.port_number
    db_po.product_name = db_prob.name

    db_supp = db_read_supp(db=db, supp_taxid = db_prob.supplier_taxid)
    db_po.supplier_taxid = db_supp.taxid
    db_po.supplier_name = db_supp.name
    db.add(db_po)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_po) # 重新整理
    return db_po

# 通過order_id刪除進貨單
def db_delete_supp_order(db: Session, order_id: int):
    res = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.order_id == order_id).delete()
    db.commit()
    return res

# -----------------------------------------------------------------------------
# 新建客戶
def db_create_cust(db: Session, cust: schemas.CustomerCreate):
    db_cust = models.Customer(  taxid = cust.taxid, name = cust.name)
    db.add(db_cust)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_cust) # 重新整理
    return db_cust

def count_cust(db: Session, cust_taxid: int):
    return db.query(models.Customer).filter(models.Customer.taxid == cust_taxid).count()

# 通過taxid查詢客戶
def db_read_cust(db: Session, cust_taxid: int):
    return db.query(models.Customer).filter(models.Customer.taxid == cust_taxid).first()

# 修改客戶
def db_update_cust(db: Session, cust_taxid: int, cust: schemas.Customer):
    db_cust = db.query(models.Customer).filter(models.Customer.taxid == cust_taxid).first()
    db_cust.taxid = cust.taxid
    db_cust.name = cust.name
    db.add(db_cust)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_cust) # 重新整理
    return db_cust

# 刪除客戶
def db_delete_cust(db: Session, cust_taxid: int):
    res = db.query(models.Customer).filter(models.Customer.taxid == cust_taxid).delete()
    db.commit()
    return res

# -----------------------------------------------------------------------------
