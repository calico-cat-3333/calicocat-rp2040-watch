import time
from micropython import const
import gc

from .log import log
from . import hal
from .task_scheduler import Task

_RECORD_PERIOD = const(10 * 60 * 1000) # 暂定每 10 分钟记录一次
MAX_RECORD = const(144 * 2)

# 简易步数记录，暂时不写存储功能了先，只记录两天的步数
# 用来同步数据到手机，之后也可以在别的地方用

step_buf = []

_lstp = 0
def record_func():
    global _lstp
    stp = hal.imu.get_step()
    stpd = stp - _lstp
    _lstp = stp
    if stpd != 0:
        if buf_any() > MAX_RECORD:
            step_buf.pop(0)
        # 算是一点小优化吧，stpd 是 10 分钟内走过的步数，正常人类应该不会超过 0xffff
        step_buf.append((time.time() << 16) + stpd)
    gc.collect()

def clear_buf():
    step_buf.clear()
    _lstp = 0

def buf_any():
    return len(step_buf)

def buf_pop():
    r = step_buf.pop(0)
    return (r >> 16, r & 0xffff)

def get_buf():
    return step_buf

def start():
    global record_task
    record_task = Task(record_func, _RECORD_PERIOD)
    record_task.start()