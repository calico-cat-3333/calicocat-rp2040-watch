import lvgl as lv
import lv_utils
import tft_config
# import tft_config_p as tft_config
import time

def timed_function(f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        t = time.ticks_us()
        result = f(*args, **kwargs)
        delta = time.ticks_diff(time.ticks_us(), t)
        print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func

tft = tft_config.config(0)

color_format = lv.COLOR_FORMAT.RGB565
pixel_size = lv.color_format_get_size(color_format)
factor = 4
width = 240
height = 240

@timed_function
def ddflush_cb(disp_drv, area, color_p):
    w = area.x2 - area.x1 + 1
    h = area.y2 - area.y1 + 1
    size = w * h
    data_view = color_p.__dereference__(size * pixel_size)
    lv.draw_sw_rgb565_swap(data_view, size)
    tft.blit_buffer(data_view, area.x1, area.y1, w, h)
    disp_drv.flush_ready()

if not lv.is_initialized(): lv.init()
if not lv_utils.event_loop.is_running(): event_loop=lv_utils.event_loop()

draw_buf1 = lv.draw_buf_create(width, height // factor, color_format, 0)
draw_buf2 = lv.draw_buf_create(width, height // factor, color_format, 0)
#draw_buf2 = None

disp_drv = lv.display_create(width, height)
disp_drv.set_color_format(color_format)
disp_drv.set_draw_buffers(draw_buf1, draw_buf2)
disp_drv.set_render_mode(lv.DISPLAY_RENDER_MODE.PARTIAL)
disp_drv.set_flush_cb(ddflush_cb)

scr = lv.obj()
lv.screen_load(scr)

rect = lv.obj(scr)
rect.set_size(50, 50)
rect.set_style_bg_color(lv.color_hex(0xFF0000), 0)  # 设置矩形的背景颜色为红色
rect.align(lv.ALIGN.TOP_LEFT, 10, 0)

x = 0
y = 0
while True:
    x = (x + 1) % width
    y = (y + 2) % height
    rect.set_x(x)
    rect.set_y(y)
    time.sleep_ms(10)



