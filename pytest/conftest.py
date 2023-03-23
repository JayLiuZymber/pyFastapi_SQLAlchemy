# conftest.py
"""
https://blog.csdn.net/wyy_a/article/details/116305497
pytest cmd下執行報錯make sure your test modules/packages have valid Python names.

需要把目錄引入到sys.path下
上層目錄位置(測試對象的檔案位置)加到sys.path內
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))