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
def create_supp(db: Session, supp: schemas.SupplierCreate):
    db_supp = models.Supplier(  taxid = supp.taxid, name = supp.name)
    db.add(db_supp)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_supp) # 重新整理
    return db_supp

def count_supp(db: Session, supp_taxid: int):
    return db.query(models.Supplier).filter(models.Supplier.taxid == supp_taxid).count()

# 通過taxid查詢供應商
def read_supp(db: Session, supp_taxid: int):
    return db.query(models.Supplier).filter(models.Supplier.taxid == supp_taxid).first()

# 修改供應商
def update_supp(db: Session, supp_taxid: int, supp: schemas.Supplier):
    db_supp = db.query(models.Supplier).filter(models.Supplier.taxid == supp_taxid).first()
    db_supp.taxid = supp.taxid
    db_supp.name = supp.name
    db.add(db_supp)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_supp) # 重新整理
    return db_supp

# 刪除供應商
def delete_supp(db: Session, supp_taxid: int):
    res = db.query(models.Supplier).filter(models.Supplier.taxid == supp_taxid).delete()
    db.commit()
    return res

# -----------------------------------------------------------------------------
# 新建供應商的product
def create_supp_product(db: Session, supp_taxid: int, prod: schemas.ProductCreate):
    db_prod = models.Product(**prod.dict(), supplier_taxid = supp_taxid)
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

def count_supp_product(db: Session, port_number: int):
    return db.query(models.Product).filter(models.Product.port_number == port_number).count()

# 通過port_number查詢產品
def read_supp_product(db: Session, port_number: int):
    return db.query(models.Product).filter(models.Product.port_number == port_number).first()

def count_supp_all_product(db: Session, supp_taxid: int):
    return db.query(models.Product).filter(models.Product.supplier_taxid == supp_taxid).count()

# 讀取供應商擁有的產品
def read_supp_all_product(db: Session, supp_taxid: int, skip: int = 0, limit: int = 100):
    db_prod = db.query(models.Product).filter(models.Product.supplier_taxid == supp_taxid)
    return db_prod.offset(skip).limit(limit).all()

# 獲取所有的產品
def read_all_product(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

# 修改產品
def update_supp_product(db: Session, port_number: int, prod: schemas.ProductCreate):
    db_prod = db.query(models.Product).filter(models.Product.port_number == port_number).first()
    db_prod.port_number = prod.port_number
    db_prod.name = prod.name
    db.add(db_prod)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_prod) # 重新整理
    return db_prod

# 刪除產品
def delete_supp_product(db: Session, port_number: int):
    res = db.query(models.Product).filter(models.Product.port_number == port_number).delete()
    db.commit()
    return res

# -----------------------------------------------------------------------------
# 新增進貨單
def create_supp_order(db: Session, order: schemas.PurchaseOrderCreate):
    log.debug('')
    db_prod = read_supp_product(db=db, port_number = order.product_pn)
    db.add(db_prod)
    db_supp = read_supp(db=db, supp_taxid = db_prod.supplier_taxid)
    # db_time = DateTime(timezone=True, server_default=func.now())
    db_order = models.PurchaseOrder( #order_id = db_time.strf,\
                                    supplier_taxid = db_supp.taxid, \
                                    supplier_name = db_supp.name, \

                                    product_id = db_prod.id, \
                                    product_pn = db_prod.port_number, \
                                    product_name = db_prod.name, \

                                    cost_price = order.cost_price, \
                                    amount = order.amount, \
                                    total_price = order.cost_price * order.amount )
    db.add(db_order)
    log.debug('db\t$%d x %d', db_prod.cost_price, db_prod.amount)
    log.debug('order\t$%d x %d', order.cost_price, order.amount)
    if (db_prod.cost_price==0) & (db_prod.amount==0): #init
        db_prod.cost_price = order.cost_price
    else:
        db_prod.cost_price = \
            ((db_prod.cost_price * db_prod.amount) + (order.cost_price * order.amount))//(db_prod.amount + order.amount)
    db_prod.amount += order.amount
    log.debug('result\t$%d x %d', db_prod.cost_price, db_prod.amount)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_order) # 重新整理
    return db_order

def count_supp_order_by_id(db: Session, id: int):
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == id).count()

# 通過id查詢進貨單
def read_supp_order_by_id(db: Session, id: int):
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == id).first()

# 通過id修改進貨單
def update_supp_order_by_id(db: Session, id: int, order: schemas.PurchaseOrder):
    db_po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == id).first()
    db_po.cost_price = order.cost_price
    db_po.amount = order.amount
    db_po.total_price = order.cost_price * order.amount
    db_po.product_pn = order.product_pn

    db_prod = read_supp_product(db=db, port_number = order.product_pn)
    #todo product
    # db_prod.cost_price
    # db_prod.amount
    db_po.product_id = db_prod.id
    db_po.product_pn = db_prod.port_number
    db_po.product_name = db_prod.name

    db_supp = read_supp(db=db, supp_taxid = db_prod.supplier_taxid)
    db_po.supplier_taxid = db_supp.taxid
    db_po.supplier_name = db_supp.name
    db.add(db_po)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_po) # 重新整理
    return db_po

# 通過id刪除進貨單
def delete_supp_order_by_id(db: Session, id: int):
    res = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == id).delete()
    db.commit()
    return res

# -----------------------------------------------------------------------------
def count_supp_order_by_supp(db: Session, supplier_taxid: int):
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.supplier_taxid == supplier_taxid).count()

def count_supp_order(db: Session, order_id: int):
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.order_id == order_id).count()

# 通過order_id查詢進貨單
def read_supp_order(db: Session, order_id: int):
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.order_id == order_id).first()

# 通過order_id修改客戶
def update_supp_order(db: Session, order_id: int, order: schemas.PurchaseOrder):
    db_po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.order_id == order_id).first()
    db_po.cost_price = order.cost_price
    db_po.amount = order.amount
    db_po.total_price = order.cost_price * order.amount
    db_po.product_pn = order.product_pn

    db_prod = read_supp_product(db=db, port_number = order.product_pn)
    #todo product
    # db_prod.cost_price
    # db_prod.amount
    db_po.product_id = db_prod.id
    db_po.product_pn = db_prod.port_number
    db_po.product_name = db_prod.name

    db_supp = read_supp(db=db, supp_taxid = db_prod.supplier_taxid)
    db_po.supplier_taxid = db_supp.taxid
    db_po.supplier_name = db_supp.name
    db.add(db_po)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_po) # 重新整理
    return db_po

# 通過order_id刪除進貨單
def delete_supp_order(db: Session, order_id: int):
    res = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.order_id == order_id).delete()
    db.commit()
    return res

# -----------------------------------------------------------------------------
# 新建客戶
def create_cust(db: Session, cust: schemas.CustomerCreate):
    db_cust = models.Customer(  taxid = cust.taxid, name = cust.name)
    db.add(db_cust)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_cust) # 重新整理
    return db_cust

def count_cust(db: Session, cust_taxid: int):
    return db.query(models.Customer).filter(models.Customer.taxid == cust_taxid).count()

# 通過taxid查詢客戶
def read_cust(db: Session, cust_taxid: int):
    return db.query(models.Customer).filter(models.Customer.taxid == cust_taxid).first()

# 修改客戶
def update_cust(db: Session, cust_taxid: int, cust: schemas.Customer):
    db_cust = db.query(models.Customer).filter(models.Customer.taxid == cust_taxid).first()
    db_cust.taxid = cust.taxid
    db_cust.name = cust.name
    db.add(db_cust)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_cust) # 重新整理
    return db_cust

# 刪除客戶
def delete_cust(db: Session, cust_taxid: int):
    res = db.query(models.Customer).filter(models.Customer.taxid == cust_taxid).delete()
    db.commit()
    return res

# -----------------------------------------------------------------------------
# 新增出貨單
def create_cust_order(db: Session, order: schemas.SaleOrderCreate):
    try:
        log.debug('')
        db_prod = read_supp_product(db, port_number = order.product_pn)
        db_cust = read_cust(db, cust_taxid = order.customer_taxid)
        db_order = models.SaleOrder(    customer_taxid = db_cust.taxid, \
                                        customer_name = db_cust.name, \

                                        product_id = db_prod.id, \
                                        product_pn = db_prod.port_number, \
                                        product_name = db_prod.name, \

                                        sale_price = order.sale_price, \
                                        amount = order.amount, \
                                        total_price = order.sale_price * order.amount )
        db.add(db_order)
        if (db_prod.sale_price==0) & (db_prod.sale_amount==0): #init
            db_prod.sale_price = order.sale_price
        else:
            db_prod.sale_price = \
                ((db_prod.sale_price * db_prod.sale_amount) + (order.sale_price * order.amount))//(db_prod.sale_amount + order.amount)
        db_prod.sale_amount +=  order.amount
        db_prod.amount = db_prod.amount - order.amount
        db.add(db_prod)
        db.commit() # 提交儲存到資料庫中
        db.refresh(db_order) # 重新整理
        return db_order
    except Exception as e:
        log.error('%s', e)
        return None

def count_cust_order_by_id(db: Session, id: int):
    return db.query(models.SaleOrder).filter(models.SaleOrder.id == id).count()

# 通過id查詢出貨單
def read_cust_order_by_id(db: Session, id: int):
    return db.query(models.SaleOrder).filter(models.SaleOrder.id == id).first()

# 通過id修改出貨單
def update_cust_order_by_id(db: Session, id: int, order: schemas.SaleOrder):
    db_so = db.query(models.SaleOrder).filter(models.SaleOrder.id == id).first()
    db_so.sale_price = order.sale_price
    db_so.amount = order.amount
    db_so.total_price = order.sale_price * order.amount
    db_so.product_pn = order.product_pn

    db_prod = read_supp_product(db, port_number = order.product_pn)
    #todo product
    # db_prod.cost_price
    # db_prod.amount
    db_so.product_id = db_prod.id
    db_so.product_pn = db_prod.port_number
    db_so.product_name = db_prod.name

    db_cust = read_cust(db, cust_taxid = order.customer_taxid)
    db_so.customer_taxid = db_cust.taxid
    db_so.customer_name = db_cust.name
    db.add(db_so)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_so) # 重新整理
    return db_so

# 通過id刪除出貨單
def delete_cust_order_by_id(db: Session, id: int):
    res = db.query(models.SaleOrder).filter(models.SaleOrder.id == id).delete()
    db.commit()
    return res

def count_cust_order_by_cust(db: Session, customer_taxid: int):
    return db.query(models.SaleOrder).filter(models.SaleOrder.customer_taxid == customer_taxid).count()

def count_cust_order(db: Session, order_id: int):
    return db.query(models.SaleOrder).filter(models.SaleOrder.order_id == order_id).count()

# 通過order_id查詢出貨單
def read_cust_order(db: Session, order_id: int):
    return db.query(models.SaleOrder).filter(models.SaleOrder.order_id == order_id).first()

# 通過order_id修改出貨單
def update_cust_order(db: Session, order_id: int, order: schemas.SaleOrder):
    db_so = db.query(models.SaleOrder).filter(models.SaleOrder.order_id == order_id).first()
    db_so.sale_price = order.sale_price
    db_so.amount = order.amount
    db_so.total_price = order.sale_price * order.amount
    db_so.product_pn = order.product_pn

    db_prod = read_supp_product(db, port_number = order.product_pn)
    #todo product
    # db_prod.cost_price
    # db_prod.amount
    db_so.product_id = db_prod.id
    db_so.product_pn = db_prod.port_number
    db_so.product_name = db_prod.name

    db_cust = read_cust(db, cust_taxid = order.customer_taxid)
    db_so.customer_taxid = db_cust.taxid
    db_so.customer_name = db_cust.name
    db.add(db_so)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_so) # 重新整理
    return db_so

# 通過order_id刪除出貨單
def delete_cust_order(db: Session, order_id: int):
    res = db.query(models.SaleOrder).filter(models.SaleOrder.order_id == order_id).delete()
    db.commit()
    return res

# -----------------------------------------------------------------------------
