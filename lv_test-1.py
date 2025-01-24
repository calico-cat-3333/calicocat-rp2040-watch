import lvgl as lv
import lv_utils
import st7789py as st7789
import tft_config

print(1)
tft = tft_config.config(0)

color_format = lv.COLOR_FORMAT.RGB565
pixel_size = lv.color_format_get_size(color_format)
factor = 4
width = 240
height = 240

print(2)
def ddflush_cb(disp_drv, area, color_p):
    w = area.x2 - area.x1 + 1
    h = area.y2 - area.y1 + 1
    size = w * h
    data_view = color_p.__dereference__(size * pixel_size)
    lv.draw_sw_rgb565_swap(data_view, size)
    tft.blit_buffer(data_view, area.x1, area.y1, w, h)
    disp_drv.flush_ready()

print(3)
if not lv.is_initialized(): lv.init()
print(3.5)
print(lv_utils.event_loop.is_running())
if not lv_utils.event_loop.is_running(): event_loop=lv_utils.event_loop()

print(4)
draw_buf1 = lv.draw_buf_create(width, height // factor, color_format, 0)
draw_buf2 = lv.draw_buf_create(width, height // factor, color_format, 0)

print(5)
disp_drv = lv.display_create(width, height)
disp_drv.set_color_format(color_format)
disp_drv.set_draw_buffers(draw_buf1, draw_buf2)
disp_drv.set_render_mode(lv.DISPLAY_RENDER_MODE.PARTIAL)
disp_drv.set_flush_cb(ddflush_cb)

print(6)
scr = lv.obj()
label = lv.label(scr)
label.set_text("Hello, LVGL!")
label.center()

print(7)
lv.screen_load(scr)
