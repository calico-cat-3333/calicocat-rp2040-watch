import lvgl as lv
#import lv_utils
import fs_driver
import time

from . import hal
from . import task_scheduler
from . import daily_scheduler
from . import lv_eventloop
from .watchface import WatchFaceAtivity


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
    load_lvgl()
    print('lvgl loaded')
    load_system_service()
    print('system service loaded')
    load_apps()
    print('apps load')

    # todo: start watchface activity
    wf = WatchFaceAtivity()
    wf.launch()
    print('launch watchface, start task_scheduler')

    while True:
        try:
            task = task_scheduler.get_due_task()
            if task != None:
                task()
            else:
                time.sleep_ms(1)
        except Exception as e:
            print(e)
