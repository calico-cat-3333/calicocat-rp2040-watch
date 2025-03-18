import lvgl as lv
import micropython

from machine import Pin

from . import Device_lv
from .cst816s import CST816S

# CST816S 触摸屏 lvgl 驱动接口

class CST816S_lv(Device_lv):
    def __init__(self, i2c, int_pin, rst_pin, use_irq=True):
        self.int_pin = int_pin
        self.tp_drv = CST816S(i2c, int_pin, rst_pin, sleep=use_irq)
        self.use_irq = use_irq

    def after_lvgl_init(self):
        self.indev_drv = lv.indev_create()
        self.indev_drv.set_type(lv.INDEV_TYPE.POINTER)
        self.need_read = False
        if self.use_irq:
            self.int_pin.irq(handler=self.tp_int_cb, trigger=Pin.IRQ_FALLING)
            self.indev_drv.set_read_cb(self.irq_touch_read_cb)
        else:
            self.indev_drv.set_read_cb(self.touch_read_cb)

    def tp_int_cb(self, pin):
        self.need_read = True

    def irq_touch_read_cb(self, indev_drv, data):
        if self.need_read and self.tp_drv.get_fingernum(): # 排除一些极端情况
            xpos, ypos = self.tp_drv.get_point()
            # rotate 270 degree
            data.point.x = 240 - ypos
            data.point.y = xpos
            data.state = lv.INDEV_STATE.PRESSED
        else:
            data.state = lv.INDEV_STATE.RELEASED
        self.need_read = False

    def touch_read_cb(self, indev_drv, data):
        if self.tp_drv.get_fingernum():
            xpos, ypos = self.tp_drv.get_point()
            # rotate 270 degree
            data.point.x = 240 - ypos
            data.point.y = xpos
            data.state = lv.INDEV_STATE.PRESSED
        else:
            data.state = lv.INDEV_STATE.RELEASED

    # 当系统睡眠或唤醒时执行
    def on_sleep():
        # Disable irq
        self.int_pin.irq(handler=None, trigger=Pin.IRQ_FALLING)

    def on_wakeup():
        # Enable irq
        self.int_pin.irq(handler=self.tp_int_cb, trigger=Pin.IRQ_FALLING)
