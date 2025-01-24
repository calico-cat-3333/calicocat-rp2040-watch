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

def drag_event_cb(e):
    target = e.get_target_obj()
    indev = lv.indev_active()
    vect = lv.point_t()
    indev.get_vect(vect)
    x = target.get_x_aligned() + vect.x
    y = target.get_y_aligned() + vect.y
    target.set_pos(x, y)

# Create a draggable object
drag_obj = lv.obj(scr)
drag_obj.set_size(70, 70)
drag_obj.set_style_bg_color(lv.color_hex(0xFF0000), 0)  # Red background
drag_obj.align(lv.ALIGN.CENTER, 0, 0)  # Center it on the screen

drag_obj.add_event_cb(drag_event_cb, lv.EVENT.PRESSING, None)

