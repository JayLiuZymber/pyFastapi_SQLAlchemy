# crud.py
'''
資料庫操作相關
通過傳入資料庫連線以及引數等進行資料庫操作，
包括建立使用者、查詢使用者等，返回的是orm模型物件
'''

from sqlalchemy.orm import Session
import models, schemas

# -----------------------------------------------------------------------------
# DB 通過taxid查詢客戶
def get_supp(db: Session, supp_taxid: int):
    return db.query(models.Supplier).filter(models.Supplier.taxid == supp_taxid).first()

# DB 新建供應商
def db_create_supp(db: Session, supp: schemas.SupplierCreate):
    db_supp = models.Supplier(taxid=supp.taxid, name=supp.name)
    db.add(db_supp)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_supp) # 重新整理
    return db_supp

# -----------------------------------------------------------------------------
# DB 獲取供應商擁有的product
def get_product(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

# DB 新建供應商的product
def db_create_supp_product(db: Session, product: schemas.ProductCreate, supp_taxid: int):
    db_product = models.Product(**product.dict(), supplier_taxid=supp_taxid)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# -----------------------------------------------------------------------------
# DB 通過taxid查詢客戶
def get_cust(db: Session, cust_taxid: int):
    return db.query(models.Customer).filter(models.Customer.taxid == cust_taxid).first()

# DB 新建客戶
def db_create_cust(db: Session, cust: schemas.CustomerCreate):
    db_cust = models.Customer(taxid=cust.taxid, name=cust.name)
    db.add(db_cust)
    db.commit() # 提交儲存到資料庫中
    db.refresh(db_cust) # 重新整理
    return db_cust
""" 
# -----------------------------------------------------------------------------
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

# 獲取使用者擁有的item
def get_item(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# 新建使用者的item
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item """
