import time
import machine
import lvgl as lv
from micropython import const, schedule

from . import hal, settingsdb
from .log import log
from .task_scheduler import Task
from .activity import current_activity

sys_sleeping = False
allow_sleep = True
_SLEEP_CHECK_PERIOD = const(1000)

def check_sleep():
    global sys_sleeping
    timeout = settingsdb.get('screenoff_timeout', 30)
    if allow_sleep and hal.dispdev.disp_drv.get_inactive_time() // 1000 > timeout:
        if not sys_sleeping:
            log('system sleep')
            sys_sleeping = True
            hal.on_sleep()
            current_activity().on_covered()
    else:
        if sys_sleeping:
            log('system wakeup')
            sys_sleeping = False
            current_activity().on_cover_exit()
            hal.on_wakeup()

def try_wakeup():
    # 程序中尝试主动唤醒显示器
    # 例如熄屏状态下尝试弹出窗口，比如闹钟到点时
    global sys_sleeping
    if sys_sleeping:
        log('system wakeup')
        lv.display_get_default().trigger_activity()
        sys_sleeping = False
        current_activity().on_cover_exit()
        hal.on_wakeup()

def prevent_sleep(v=None):
    # 阻止系统睡眠
    global allow_sleep
    if v == None:
        return not allow_sleep
    allow_sleep = not v
    return v

def start():
    global sleep_check_task
    sleep_check_task = Task(check_sleep, _SLEEP_CHECK_PERIOD)
    sleep_check_task.start()