import lvgl as lv
import lv_utils
import fs_driver

from . import hal
from . import task_scheduler

class CCES:
    def __init__(self):
        pass

    def load_lvgl(self):
        lv.init()
        self.lv_event_loop = lv_utils.event_loop()
        self.fs_drv = lv.fs_drv_t()
        fs_driver.fs_register(fs_drv, 'S')
        hal.after_lvgl_init()