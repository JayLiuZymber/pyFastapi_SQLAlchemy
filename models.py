# models.py
'''
資料庫模型表
通過資料庫配置檔案中的基類來建立模型類
複雜例項 在之前的基礎上再加一個模型類Item，User與之是一對多的關係
'''

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# 商品
class Product(Base):
    __tablename__ = "products" #"goods"
    id = Column(Integer, primary_key=True, index=True)
    port_number = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    supplier_taxid = Column(Integer, ForeignKey("suppliers.taxid"))
    supplier = relationship("Supplier", back_populates="products")

    cost_price = Column(Integer, nullable=False)
    sell_price = Column(Integer, nullable=False)
    amount = Column(Integer, default=0)

# 供應商
class Supplier(Base):
    __tablename__ = "suppliers"
    # id = Column(Integer, primary_key=True, index=True)
    # 統一編號
    taxid = Column(Integer, primary_key=True, unique=True, index=True, nullable=False, autoincrement=False)
    name = Column(String(32), unique=True, nullable=False)
    
    products = relationship("Product", back_populates="supplier")

# 進貨單
class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, index=True)
    # supplier_taxid = Column(Integer, nullable=False)
    # supplier = Column(String(32), nullable=False)
    supplier_taxid = Column(Integer, ForeignKey("suppliers.taxid"), nullable=False)
    supplier = Column(String(32), ForeignKey("suppliers.name"), nullable=False)

    # product_taxid = Column(Integer, nullable=False)
    # product = Column(String(32), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable=False)
    product = Column(String(32), ForeignKey("products.name"), nullable=False)

    cost_price = Column(Integer, default=0, nullable=False)
    amount = Column(Integer, default=0, nullable=False)
    total_price = Column(Integer, nullable=False)

# -----------------------------------------------------------------------------
# 客戶
class Customer(Base):
    __tablename__ = "customers"
    # id = Column(Integer, primary_key=True, index=True)
    # 統一編號
    taxid = Column(Integer, primary_key=True, unique=True, index=True, nullable=False, autoincrement=False)
    name = Column(String(32), unique=True, nullable=False)

# 出貨單
class SellOrder(Base):
    __tablename__ = "sell_orders"
    id = Column(Integer, primary_key=True, index=True)
    # customer_taxid = Column(Integer, nullable=False)
    # customer = Column(String(32), nullable=False)
    customer_taxid = Column(Integer, ForeignKey("customers.taxid"), index=True, nullable=False)
    customer = Column(String(32), ForeignKey("customers.name"), nullable=False)

    # product_id = Column(Integer, nullable=False)
    # product = Column(String(32), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable=False)
    product = Column(String(32), ForeignKey("products.name"), nullable=False)

    sell_price = Column(Integer, default=0)
    amount = Column(Integer, default=0, nullable=False)
    total_price = Column(Integer, nullable=False)

# -----------------------------------------------------------------------------
