import lvgl as lv
#import lv_utils
import fs_driver
import time

from . import hal
from . import task_scheduler
from . import daily_scheduler
from . import lv_eventloop
from .watchface import WatchFaceAtivity

from .log import log


def load_lvgl():
    global lv_event_loop
    global fs_driver
    lv.init()
    #lv_event_loop = lv_utils.event_loop()
    lv_event_loop = lv_eventloop.start()
    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'S')
    hal.after_lvgl_init()

def load_system_service():
    daily_scheduler.start()

def load_apps():
    # todo: load apps
    pass

def start():
    log('start system')
    load_lvgl()
    log('lvgl loaded')
    load_system_service()
    log('system service loaded')
    load_apps()
    log('apps load')

    # todo: start watchface activity
    wf = WatchFaceAtivity()
    wf.launch()
    log('launch watchface, start task_scheduler')

    while True:
        task = task_scheduler.get_due_task()
        if task != None:
            task()
        else:
            time.sleep_ms(1)