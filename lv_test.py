import lvgl as lv
import lv_utils
import board
import tft_config
import tp_config
import time
import gc


tft = tft_config.config(0)

color_format = lv.COLOR_FORMAT.RGB565
pixel_size = lv.color_format_get_size(color_format)
factor = 4
width = 240
height = 240

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

def touch_read_cb(indev_drv, data):
    if tp.get_fingernum():
        xpos, ypos = tp.get_point()
        data.point.x = xpos
        data.point.y = ypos
        data.state = lv.INDEV_STATE.PRESSED
    else:
        data.state = lv.INDEV_STATE.RELEASED

tp = tp_config.config()
indev_drv = lv.indev_create()
indev_drv.set_type(lv.INDEV_TYPE.POINTER)
indev_drv.set_read_cb(touch_read_cb)

scr = lv.obj()
lv.screen_load(scr)

button1 = lv.button(scr)
button1.align(lv.ALIGN.CENTER, 0, -50)
label = lv.label(button1)
label.set_text("Click Me!!!")

t = 0
def button1_event_cb(event):
    global t
    t = t + 1
    c_label.set_text(str(t))
    print("button1 clicked", t)
    
button1.add_event_cb(button1_event_cb, lv.EVENT.CLICKED, None)

c_label = lv.label(scr)
c_label.align(lv.ALIGN.CENTER, 0, 0)
c_label.set_text(str(t))


mem_label = lv.label(scr)
mem_label.align(lv.ALIGN.LEFT_MID, 40, 30)
mem_label.set_text('mem useage')

def get_mem():
    m = gc.mem_free() / 1024
    return 'mem_free: ' + str(m) + 'KB'

while True:
    m = get_mem()
    print(m)
    mem_label.set_text(m)
    time.sleep_ms(500)