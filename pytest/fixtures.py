# fixture.py
""" 
https://ithelp.ithome.com.tw/articles/10295781
Python 與自動化測試的敲門磚_Day08_Pytest 與 In-memory SQLite

建立 fixture
接下來就是重點了，sqlalchemy 實際對資料庫進行操作的時後，需要一個 session 物件來協助我們進行操作，
接下來我們就要利用 fixture 來替我們在測試前做建立資料表以及產生一個 session 的動作

程式解析：
    利用剛剛所介紹的方法，先建立一個 engine 並與虛擬的 sqlite 進行連線
    在測試之前我們先利用 fixture 替我們將資料表建立好，這樣在測試的過程中就不需要再花時間在撰寫建立環境的部分
    接著我們實際建立一個 session 並 yield 出去
        使用 yield 的原因是，當 test case 結束後，就會回到 fixture 內執行接下來的動作
        由於式使用 with 進行 session 的建立，因此也 test case 結束後回到 fixture 內，此 session 會自動關閉
    最後 test case 結束會到 fixture 內將資料表全部刪除，確保下一個 test case 有乾淨的環境做測試

安裝套件
pip install pytest

https://ithelp.ithome.com.tw/articles/10307902
Python 與自動化測試的敲門磚_Day29_Pytest 與併發測試
安裝套件
pip install pytest-xdist
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Base

@pytest.fixture(name='sqlite_session')
def sqlite_session_fixture() -> Session:
    # 建立 engine
    engine_url = "sqlite://"
    engine = create_engine(engine_url)

    # 建立資料表
    Base.metadata.create_all(engine)
    
    #  yield 出 Session
    with sessionmaker(bind=engine)() as session:
        yield session
        
    # 刪除資料表
    Base.metadata.drop_all(engine)
    