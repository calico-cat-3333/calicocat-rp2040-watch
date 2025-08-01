import cst816s
import lvgl as lv
import micropython
from machine import Pin

class CST816S_lv:
    def __init__(self, i2c, int_pin, rst_pin, use_irq=True):
        if not lv.is_initialized():
            lv.init()

        self.int_pin = int_pin
        self.tp_drv = cst816s.CST816S(i2c, int_pin, rst_pin, sleep=use_irq)
        self.indev_drv = lv.indev_create()
        self.indev_drv.set_type(lv.INDEV_TYPE.POINTER)
        self.need_read = False
        if use_irq:
            self.int_pin.irq(handler=self.tp_int_cb, trigger=Pin.IRQ_FALLING)
            self.indev_drv.set_read_cb(self.irq_touch_read_cb)
        else:
            self.indev_drv.set_read_cb(self.touch_read_cb)

    def tp_int_cb(self, pin):
        self.need_read = True

    def irq_touch_read_cb(self, indev_drv, data):
        if self.need_read and self.tp_drv.get_fingernum(): # 排除一些极端情况
            xpos, ypos = self.tp_drv.get_point()
            data.point.x = xpos
            data.point.y = ypos
            data.state = lv.INDEV_STATE.PRESSED
        else:
            data.state = lv.INDEV_STATE.RELEASED
        self.need_read = False

    def touch_read_cb(self, indev_drv, data):
        if self.tp_drv.get_fingernum():
            xpos, ypos = self.tp_drv.get_point()
            data.point.x = xpos
            data.point.y = ypos
            data.state = lv.INDEV_STATE.PRESSED
        else:
            data.state = lv.INDEV_STATE.RELEASED

    # 当系统睡眠或唤醒时执行
    def on_sleep():
        pass

    def on_wakeup():
        pass
