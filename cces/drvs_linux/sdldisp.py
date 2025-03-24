import lvgl as lv
from . import Device_lv
from ..log import log

class SDLdisp(Device_lv):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.brightness = 100

    def after_lvgl_init(self):
        lv.sdl_window_create(self.width, self.height)
        log("Running the SDL lvgl version")

    def on_wakeup(self):
        log('sdl dispdev wakeup')

    def on_sleep(self):
        log('sdl dispdev sleep')

    def set_brightness(self, value):
        if value >= 100:
            self.brightness = 100
        elif value <= 0:
            self.brightness = 1
        else:
            self.brightness = value