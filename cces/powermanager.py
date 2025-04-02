import time
import machine
from micropython import const, schedule

from . import hal, settingsdb
from .log import log
from .task_scheduler import Task

sys_sleeping = False
allow_sleep = True
_SLEEP_CHECK_PERIOD = const(1000)

def check_sleep(_):
    global sys_sleeping
    timeout = settingsdb.get('screenoff_timeout', 30)
    if allow_sleep and hal.dispdev.disp_drv.get_inactive_time() // 1000 > timeout:
        if not sys_sleeping:
            log('system sleep')
            sys_sleeping = True
            hal.on_sleep()
    else:
        if sys_sleeping:
            log('system wakeup')
            sys_sleeping = False
            hal.on_wakeup()

def schedule_check_sleep():
    # try_wakeup 可能在中断服务函数中执行，为了保证所有睡眠和唤醒操作的原子性，这里需要使用这种方法实现。
    schedule(check_sleep, 0)

def try_wakeup():
    # 程序中尝试主动唤醒显示器
    # 例如熄屏状态下尝试弹出窗口，比如闹钟到点时
    global sys_sleeping
    if sys_sleeping:
        log('system wakeup')
        lv.display_get_default().trigger_activity()
        sys_sleeping = False
        hal.on_wakeup()

def prevent_sleep(v=None):
    global allow_sleep
    if v == None:
        return not allow_sleep
    allow_sleep = not v
    return v

def start():
    global sleep_check_task
    sleep_check_task = Task(schedule_check_sleep, _SLEEP_CHECK_PERIOD)
    sleep_check_task.start()