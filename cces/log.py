import sys

from time import ticks_ms

# 日志系统
# 使用方法：
# from log import log, ERROR
# log('msg', var, level=ERROR)
# log('msg', var)
# try:
#     (do sth)
# except Exception as e:
#     log('msg', e, exc=e, level=ERROR)

INFO = 0
ERROR = 1
NOLOG = 2
levelstr = [' INFO:', 'ERROR:', 'NOLOG:']

_level = ERROR

def setlevel(level):
    global _level
    _level = level

def log(*args, level=INFO, exc=None, **kwargs):
    if  _level > level or level == NOLOG:
        return
    print('[' + str(ticks_ms()) + ']', levelstr[level], *args, **kwargs)
    if exc == None:
        return
    sys.print_exception(exc)