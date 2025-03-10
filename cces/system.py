import lvgl as lv
import lv_utils
import fs_driver
import time

from . import hal
from . import task_scheduler
from . import daily_scheduler

class CCES:
    def __init__(self):
        pass

    def load_lvgl(self):
        lv.init()
        self.lv_event_loop = lv_utils.event_loop()
        self.fs_drv = lv.fs_drv_t()
        fs_driver.fs_register(fs_drv, 'S')
        hal.after_lvgl_init()

    def load_system_service(self):
        daily_scheduler.start()

    def load_apps(self):
        # todo: load apps
        pass

    def start(self):
        self.load_lvgl()
        self.load_system_service()
        self.load_apps()

        # todo: start watchface activity

        while True:
            task = task_scheduler.get_due_task()
            if task != None:
                task()
            else:
                time.sleep_ms(1)
