"""RP2040-Touch-LCD-1.28
"""

import board
import gc9a01
import lvgl as lv
from machine import PWM
import time
from ..hal import Device_lv

class GC9A01_lv(Device_lv):
    def __init__(self, spi, rst, cs, dc, bl, doublebuffer=True):
        self.width = 240
        self.height = 240
        self.doublebuffer = doublebuffer

        self.tft_drv = gc9a01.GC9A01(
            spi,
            self.width,
            self.height,
            reset=rst,
            cs=cs,
            dc=dc,
            rotation=3, #270 degree
            options=0,
            buffer_size=0
        )
        self.tft_drv.init()

        self.bl_pin = bl
        if bl is not None:
            self.backlight = PWM(bl)
            self.brightness = 65535
            self.backlight.freq(5000)
            self.backlight.duty_u16(self.brightness)
            self.brightness_range = [500,65535]

    def after_lvgl_init(self):
        self.color_format = lv.COLOR_FORMAT.RGB565
        self.pixel_size = lv.color_format_get_size(self.color_format)
        self.factor = 4

        self.draw_buf1 = lv.draw_buf_create(self.width, self.height // self.factor, self.color_format, 0)
        self.draw_buf2 = lv.draw_buf_create(self.width, self.height // self.factor, self.color_format, 0) if self.doublebuffer else None

        self.disp_drv = lv.display_create(self.width, self.height)
        self.disp_drv.set_color_format(self.color_format)
        self.disp_drv.set_draw_buffers(self.draw_buf1, self.draw_buf2)
        self.disp_drv.set_render_mode(lv.DISPLAY_RENDER_MODE.PARTIAL)
        self.disp_drv.set_flush_cb(self.tft_flush_cb)

    def tft_flush_cb(self, disp_drv, area, color_p):
        w = area.x2 - area.x1 + 1
        h = area.y2 - area.y1 + 1
        size = w * h
        data_view = color_p.__dereference__(size * self.pixel_size)
        lv.draw_sw_rgb565_swap(data_view, size)
        self.tft_drv.blit_buffer(data_view, area.x1, area.y1, w, h)
        disp_drv.flush_ready()

    def set_brightness(self, value):
        if self.bl_pin == None:
            return
        if value > self.brightness_range[1]:
            value = self.brightness_range[1]
        if value < self.brightness_range[0]:
            value = self.brightness_range[0]
        self.brightness = value
        self.backlight.duty_u16(self.brightness)

    def bl_off(self):
        self.backlight.duty_u16(0)
        time.sleep_ms(1)
        self.backlight.deinit()

    def bl_on(self):
        self.backlight.duty_u16(self.brightness)

    def on_sleep(self):
        # Not yet completed.
        self.bl_off()
        self.tft_drv.sleep_mode(True)

    def on_wakeup(self):
        # Not yet completed.
        self.tft_drv.sleep_mode(False)
        self.bl_on()

