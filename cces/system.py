import lvgl as lv
import lv_utils
import fs_driver
import time

from . import hal
from . import task_scheduler
from . import daily_scheduler


def load_lvgl():
    global lv_event_loop
    global fs_driver
    lv.init()
    lv_event_loop = lv_utils.event_loop()
    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'S')
    hal.after_lvgl_init()

def load_system_service():
    daily_scheduler.start()

def load_apps():
    # todo: load apps
    pass

def start():
    load_lvgl()
    load_system_service()
    load_apps()

    # todo: start watchface activity

    while True:
        task = task_scheduler.get_due_task()
        if task != None:
            task()
        else:
            time.sleep_ms(1)
