# database.py
'''
https://www.796t.com/article.php?id=293287
以MySQL為例，SQLAlchemy需要藉助於pymysql連線資料庫，
所以需要進行安裝這兩個工具包：
pip install sqlalchemy
pip install pymysql

資料庫配置相關
在資料庫相關的配置檔案中，首先建立一個SQLAlchemy的"engine"，
然後建立SessionLocal例項進行會話，最後建立模型類的基類
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:qazqsedc/@127.0.0.1:3306/db"

# echo=True表示引擎將用repr()函式記錄所有語句及其引數列表到日誌
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

# SQLAlchemy中，CRUD是通過會話進行管理的，所以需要先建立會話，
# 每一個SessionLocal例項就是一個數據庫session
# flush指傳送到資料庫語句到資料庫，但資料庫不一定執行寫入磁碟
# commit是指提交事務，將變更儲存到資料庫檔案中
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立基本對映類
Base = declarative_base()
