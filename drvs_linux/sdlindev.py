import lvgl as lv
from cces.drvs import Device_lv
from cces.log import log

class SDLindev(Device_lv):
    def __init__(self):
        pass

    def after_lvgl_init(self):
        self.group = lv.group_create()
        self.group.set_default()
        self.mouse = lv.sdl_mouse_create()
        self.keyboard = lv.sdl_keyboard_create()
        self.keyboard.set_group(self.group)

    def on_wakeup(self):
        log('sdl indev wakeup')

    def on_sleep(self):
        log('sdl indev sleep')