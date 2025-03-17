from time import ticks_ms
import sys

INFO = 1
ERROR = 2
NOLOG = 0
levelstr = ['NOLOG:',' INFO:', 'ERROR:']

_level = ERROR

def setlevel(level):
    global _level
    _level = level

def log(*args, level=INFO, exc=None, **kwargs):
    if  _level < level or level == NOLOG:
        return
    print('[' + str(ticks_ms()) + ']', levelstr[level], *args, **kwargs)
    if exc == None:
        return
    sys.print_exception(e)