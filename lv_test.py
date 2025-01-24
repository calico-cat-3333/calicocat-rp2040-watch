import lvgl as lv
import lv_utils
import board
from gc9a01_lv import GC9A01_lv
from cst816s_lv import CST816S_lv
import time
import gc

if not lv.is_initialized(): lv.init()
if not lv_utils.event_loop.is_running(): event_loop=lv_utils.event_loop()

disp_drv = GC9A01_lv(board.lcd_spi, board.lcd_rst, board.lcd_cs, board.lcd_dc, board.lcd_bl)
tp_drv = CST816S_lv(board.i2c1, board.tp_int, board.tp_rst)

scr = lv.obj()
lv.screen_load(scr)

button1 = lv.button(scr)
button1.align(lv.ALIGN.CENTER, 0, -20)
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
c_label.align(lv.ALIGN.CENTER, 0, -70)
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