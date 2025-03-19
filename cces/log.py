import sys

from time import ticks_ms, ticks_us, ticks_diff

'''
日志系统
使用方法：
from log import log, ERROR, DEBUG
log('msg', var, level=ERROR)
log('msg', var)
try:
    (do sth)
except Exception as e:
    log('msg', e, exc=e, level=ERROR)
'''

DEBUG = 0
INFO = 1
ERROR = 2
NOLOG = 3
_levelstr = ['DEBUG:', ' INFO:', 'ERROR:', 'NOLOG:']

_level = ERROR

def setlevel(level):
    global _level
    _level = level

def log(*args, level=INFO, exc=None, **kwargs):
    if  _level > level or level == NOLOG:
        return
    print('[' + str(ticks_ms()) + ']', _levelstr[level], *args, **kwargs)
    if exc == None:
        return
    sys.print_exception(exc)

def get_time(f, *args, **kwargs):
    myname = f.__name__
    def new_func(*args, **kwargs):
        t = ticks_us()
        result = f(*args, **kwargs)
        delta = ticks_diff(ticks_us(), t)
        print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func