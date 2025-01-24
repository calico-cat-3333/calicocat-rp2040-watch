"""RP2040-Touch-LCD-1.28
"""

import board
import gc9a01
import lvgl as lv

class GC9A01_lv:
    def __init__(self, spi, rst, cs, dc, bl, doublebuffer=True):
        if not lv.is_initialized():
            lv.init()

        self.width = 240
        self.height = 240
        self.color_format = lv.COLOR_FORMAT.RGB565
        self.pixel_size = lv.color_format_get_size(self.color_format)
        self.factor = 4

        self.tft_drv = gc9a01.GC9A01(
            spi,
            self.width,
            self.height,
            reset=rst,
            cs=cs,
            dc=dc,
            rotation=0,
            options=0,
            buffer_size=0
        )
        self.tft_drv.init()

        self.backlight = bl
        if self.backlight is not None:
            self.backlight.value(1)

        self.draw_buf1 = lv.draw_buf_create(self.width, self.height // self.factor, self.color_format, 0)
        self.draw_buf2 = lv.draw_buf_create(self.width, self.height // self.factor, self.color_format, 0) if doublebuffer else None

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

    def set_backlight_value(self, brightness):
        if brightness > 100:
            brightness = 100
        if brightness < 10:
            brightness = 10

