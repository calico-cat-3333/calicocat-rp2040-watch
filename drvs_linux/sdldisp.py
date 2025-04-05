import lvgl as lv
from . import Device_lv
from cces.log import log

class SDLdisp(Device_lv):
    def __init__(self, width, height, zoom=1):
        self.width = width
        self.height = height
        self.brightness = 100
        self.zoom = zoom

    def after_lvgl_init(self):
        self.disp_drv = lv.sdl_window_create(self.width, self.height)
        lv.sdl_window_set_resizeable(self.disp_drv, False)
        lv.sdl_window_set_zoom(self.disp_drv, self.zoom)
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
        log('sdl dispdev: set brightness:', self.brightness)