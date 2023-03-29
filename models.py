# models.py
'''
資料庫模型表
通過資料庫配置檔案中的基類來建立模型類
複雜例項 在之前的基礎上再加一個模型類Item，User與之是一對多的關係

SQL Data Types
https://www.digitalocean.com/community/tutorials/sql-data-types
Numeric data types such as: INT, TINYINT, BIGINT, FLOAT, REAL, etc.
Date and Time data types such as: DATE, TIME, DATETIME, etc.
Character and String data types such as: CHAR, VARCHAR, TEXT, etc.
Unicode character string data types such as: NCHAR, NVARCHAR, NTEXT, etc.
Binary data types such as: BINARY, VARBINARY, etc.
Miscellaneous data types - CLOB, BLOB, XML, CURSOR, TABLE, etc.
'''

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Double
from sqlalchemy import BIGINT
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import func
from database import Base

# 產品
class Product(Base):
    __tablename__ = "products" #"goods"
    id = Column(Integer, primary_key=True, index=True)
    port_number = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    supplier_taxid = Column(Integer, ForeignKey("suppliers.taxid", onupdate="CASCADE"), nullable=False)
    supplier = relationship("Supplier", back_populates="products")

    #成本價=進貨價
    cost_price = Column(Integer, nullable=False)
    #倉庫數
    amount = Column(Integer, default=0, nullable=False)
    sale_price = Column(Integer, nullable=False)
    #售出數
    sale_amount = Column(Integer, default=0, nullable=False)

# 供應商
class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    # 統一編號
    taxid = Column(Integer, unique=True, index=True, nullable=False, autoincrement=False)
    name = Column(String(32), unique=True, nullable=False)

    products = relationship("Product", back_populates="supplier")

# 進貨單
class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    time_id = column_property(func.date_format(time, '%Y%m%d.%H%i%s')) #=20230320.140218
    order_id = Column(BIGINT, unique=True, index=True, default=func.date_format(time, '%Y%m%d%H%i%s'), nullable=False) #=20230320140218

    # supplier_taxid = Column(Integer, nullable=False)
    # supplier = Column(String(32), nullable=False)
    supplier_taxid = Column(Integer, ForeignKey("suppliers.taxid", onupdate="CASCADE"), nullable=False)
    supplier_name = Column(String(32), ForeignKey("suppliers.name", onupdate="CASCADE"), nullable=False)

    # product_taxid = Column(Integer, nullable=False)
    # product = Column(String(32), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", onupdate="CASCADE"), index=True, nullable=False)
    product_pn = Column(Integer, ForeignKey("products.port_number", onupdate="CASCADE"), index=True, nullable=False)
    product_name = Column(String(32), ForeignKey("products.name", onupdate="CASCADE"), nullable=False)

    cost_price = Column(Integer, default=0, nullable=False)
    amount = Column(Integer, default=0, nullable=False)
    total_price = Column(Integer, default=0, nullable=False)

# -----------------------------------------------------------------------------
# 客戶
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    # 統一編號
    taxid = Column(Integer, unique=True, index=True, nullable=False, autoincrement=False)
    name = Column(String(32), unique=True, nullable=False)

# 出貨單
class SellOrder(Base):
    __tablename__ = "sale_orders"
    id = Column(Integer, primary_key=True, index=True)

    time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    time_id = column_property(func.date_format(time, '%Y%m%d.%H%i%s')) #=20230320.140218
    order_id = Column(BIGINT, unique=True, index=True, default=func.date_format(time, '%Y%m%d%H%i%s'), nullable=False) #=20230320140218

    # customer_taxid = Column(Integer, nullable=False)
    # customer = Column(String(32), nullable=False)
    customer_taxid = Column(Integer, ForeignKey("customers.taxid"), index=True, nullable=False)
    customer_name = Column(String(32), ForeignKey("customers.name"), nullable=False)

    # product_id = Column(Integer, nullable=False)
    # product = Column(String(32), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable=False)
    product_pn = Column(Integer, ForeignKey("products.port_number"), index=True, nullable=False)
    product_name = Column(String(32), ForeignKey("products.name"), nullable=False)

    sale_price = Column(Integer, default=0, nullable=False)
    amount = Column(Integer, default=0, nullable=False)
    total_price = Column(Integer, default=0, nullable=False)

# -----------------------------------------------------------------------------
