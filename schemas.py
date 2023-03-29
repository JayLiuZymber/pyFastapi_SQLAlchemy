# schemas.py
'''
模型驗證
定義請求引數模型驗證與響應模型驗證的Pydantic模型，
其中響應模型中設定orm_mode=True引數，表示與ORM模型相容，
因為後續中返回的資料庫查詢是orm模型，
通過設定這個引數可以將orm模型通過pydantic模型進行驗證
'''

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

# -----------------------------------------------------------------------------
# 商品
class ProductBase(BaseModel):
    cost_price: int = 0
    amount: int = 0
    sale_price: int = 0
    sale_amount: int = 0

class ProductCreate(ProductBase):
	# 請求模型驗證
    port_number: int
    name: str

class Product(ProductBase):
    # 響應模型
    id: int
    supplier_taxid: int
    port_number: int
    name: str

    class Config:
        orm_mode = True

# -----------------------------------------------------------------------------
# 供應商
class SupplierBase(BaseModel):
    name: str

class SupplierCreate(SupplierBase):
    # 請求模型驗證
    taxid: int

class Supplier(SupplierBase):
    # 響應模型
    id: int
    taxid: int
    name: str
    products: List[Product] = []

    class Config:
        orm_mode = True

# -----------------------------------------------------------------------------
# 進貨單
class PurchaseOrderBase(BaseModel):
    cost_price: int
    amount: int

class PurchaseOrderCreate(PurchaseOrderBase):
    product_pn: int

class PurchaseOrder(PurchaseOrderBase):
    id: int
    time: datetime
    time_id: float
    order_id: int
    
    supplier_taxid: int
    supplier_name: str
    
    product_pn: int
    product_id: int
    product_name: str
    
    cost_price: int
    amount: int
    total_price: int

    class Config:
        orm_mode = True

# -----------------------------------------------------------------------------
# 客戶
class CustomerBase(BaseModel):
    name: str

class CustomerCreate(CustomerBase):
    taxid: int

class Customer(CustomerBase):
    id: int
    taxid: int
    name: str

    class Config:
        orm_mode = True

# -----------------------------------------------------------------------------
# 出貨單
class SaleOrderBase(BaseModel):
    sale_price: int
    amount: int

class SaleOrderCreate(SaleOrderBase):
    customer_taxid: int
    product_pn: int

class SaleOrder(SaleOrderBase):
    id: int
    time: datetime
    time_id: float
    order_id: int

    customer_taxid: int
    customer_name: str
    
    product_pn: int
    product_id: int
    product_name: str

    sale_price: int
    amount: int
    total_price: int

    class Config:
        orm_mode = True

# -----------------------------------------------------------------------------
