# prints.py
""" by Jay
使用設定
from prints import __filename__, __line__ 
from prints import printstd, printout
"""
import inspect, os, sys
from colorama import init, Fore, Back

# -----------------------------------------------------------------------------
init(autoreset=True) #colorama

class LineNo:
    def __str__(self):
        return str(inspect.currentframe().f_back.f_lineno)
    
__line__ = LineNo() #指令所在行數
# 13

# __file__
# C:\pytest\prints.py

class FileName:
    def __str__(self):
        return os.path.basename(__file__)
    
__filename__ = FileName()
# prints.py

#e.g. printstd('xxx')
def printstd(*objects):
    # VS Code'終端機'頁使用
    # prints.py, line 20 | xxx
    print(__filename__, ', line ', __line__, Fore.YELLOW+' | ', *objects, sep='', end='\n', file=sys.stdout, flush=False)
    #=print(__filename__, ', line ', __line__, ' | ', xxx, sep='')

#e.g. printout('xxx')
def printout(*objects):
    # VS Code'輸出'頁使用
    # C:\pytest\prints.py:20 | xxx
    print(__file__, ':', __line__, '| ', *objects, sep='', end='\n', file=sys.stdout, flush=False)
    #=print(__file__, ':', __line__, ' ', xxx, sep='')

