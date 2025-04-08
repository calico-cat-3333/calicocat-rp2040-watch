import time
from micropython import const
import gc

from .log import log
from . import hal
from .task_scheduler import Task

RECORD_PERIOD = const(10 * 60 * 1000) # 暂定每 10 分钟记录一次
_MAX_RECORD = const(144)

# 简易步数记录，暂时不写存储功能了先，只记录一天的步数
# 用来同步数据到手机，之后也可以在别的地方用

step_buf = []

_lstp = 0
def record_func():
    stp = hal.imu.get_step()
    stpd = stp - _lstp
    if stpd != 0:
        if buf_any() > _MAX_RECORD:
            step_buf.pop(0)
        step_buf.append((time.time(), stpd))
    gc.collect()

def clear_buf():
    step_buf.clear()
    _lstp = 0

def buf_any():
    return len(step_buf)

def buf_pop():
    return step_buf.pop(0)

def get_buf():
    return step_buf

def start():
    global record_task
    record_task = Task(record_func, RECORD_PERIOD)
    record_task.start()