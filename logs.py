# logs.py
"""
logs 快速設定版
"""

import logging
from colorama import init, Fore, Back

CRITICAL = logging.CRITICAL
FATAL = CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

""" 
%(asctime)s	 日期時間, 格式為 YYYY-MM-DD HH:mm:SS,ms (毫秒)
%(message)s	 使用者自訂訊息
%(levelname)s	 日誌安全等級
%(levelno)s	 日誌安全等級之數值
%(name)s	 使用者名稱 (帳號) 
%(lineno)d	 日誌輸出函數呼叫於程式中所在之列數
%(filename)s	 日誌輸出函數之模組的檔名
%(module)s	 日誌輸出函數之模組名稱
%(pathname)s	 日誌輸出函數之模組之完整路徑
%(funcName)s	 日誌輸出函數之名稱
%(threrad)d	 執行緒 ID
%(threradName)s	 執行緒名稱
%(process)d	 程序 ID
%(created)f	 以 UNIX 標準表示之現在時間 (浮點數)
"""
# -----------------------------------------------------------------------------
init(autoreset=True) #colorama

def getLogger(title: str, level: int = DEBUG, toFile: bool = False):
    toStream = True

    logger: logging.Logger = logging.getLogger(name=title)
    logger.setLevel(level)

    # DEBUG:(main) main.py, line 104 | xxx
    formatter: logging.Formatter = logging.Formatter( \
        # Fore.MAGENTA + '%(levelname)s'+ Fore.RESET +':(%(name)s) %(filename)s line:%(lineno)d %(message)s')
        # Fore.MAGENTA + '%(levelname)s'+ Fore.RESET +':(%(name)s) \u001b]8;;%(filename)s\u001b\\%(filename)s\u001b]8;;\u001b\\ line:%(lineno)d %(message)s')
        # Fore.MAGENTA + '%(levelname)s'+ Fore.RESET +':(%(name)s) \x1b]8;;%(filename)s\a%(filename)s\x1b]8;;\a line:%(lineno)d %(message)s')
        # Fore.YELLOW +'%(levelname)s:(%(name)s)'+ Fore.RESET +' %(filename)s, line %(lineno)d | %(message)s')
        Fore.YELLOW +'%(levelname)s:(%(name)s)'+ Fore.RESET +' %(funcName)s | %(message)s')
    # print(f"\u001b]8;;{target}\u001b\\{text}\u001b]8;;\u001b\\")
    # print(f"\x1b]8;;{target}\a{text}\x1b]8;;\a")
    # File "{file_path}", line {line_number}
    handler: logging.StreamHandler = logging.StreamHandler()
    handler.setFormatter(formatter)

    fileformatter = formatter
    fileformatter: logging.Formatter = logging.Formatter( \
        '%(asctime)s'+ Fore.YELLOW +'%(levelname)s:(%(name)s)'+ Fore.RESET +' %(filename)s, line %(lineno)d | %(message)s')
    fileHandler: logging.FileHandler = logging.FileHandler(filename='log.ansi', encoding='utf-8', mode='w')
    fileHandler.setFormatter(fileformatter)

    if toStream:
        logger.addHandler(handler)
    if toFile:
        logger.addHandler(fileHandler)
    return logger
