import lvgl as lv
#import lv_utils
import fs_driver
import time
import gc

from . import hal
from . import task_scheduler
from . import daily_scheduler
from . import lv_eventloop
from . import settingsdb
from . import gadgetbridge
from . import appmgr
from . import powermanager
#from . import steprecord
from .watchface import WatchFaceAtivity
from .log import log
from .activity import styles

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
    settingsdb.start()
    gadgetbridge.start()
    styles.start()
    powermanager.start()
    #steprecord.start()

def start():
    log('start system')
    load_lvgl()
    log('lvgl loaded')
    load_system_service()
    log('system service loaded')
    appmgr.load_apps()
    log('apps loaded')

    gc.collect()

    wf = WatchFaceAtivity()
    wf.launch()
    log('launch watchface, start task_scheduler')

    task_scheduler.start()