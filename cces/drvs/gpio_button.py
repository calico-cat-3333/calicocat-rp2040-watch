import micropython
import lvgl as lv
from machine import Pin

from . import Device_lv
from .. import powermanager

# 这不是标准的 lvgl 输入设备，在 lvgl 输入设备的基础上扩展了从睡眠中唤醒的功能
class GPIOButton(Device_lv):
    def __init__(self, pin):
        self.pin = pin
        self.pin.irq(handler=self.int_pin_read, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.pressed = False
        self.onwakeup = False

    def int_pin_read(self, pin):
        if pin.value():
            self.pressed = False
        else:
            self.pressed = True

    def after_lvgl_init(self):
        self.indev_drv = lv.indev_create()
        self.indev_drv.set_type(lv.INDEV_TYPE.KEYPAD)
        self.indev_drv.set_read_cb(self.button_read_cb)
        self.group = lv.group_create()
        self.group.set_default()
        self.indev_drv.set_group(self.group)

    def button_read_cb(self, indev_drv, data):
        if self.pressed:
            if powermanager.sys_sleeping:
                powermanager.try_wakeup() # 如果是唤醒，则不进行任何操作
                data.state = lv.INDEV_STATE.RELEASED
                self.onwakeup = True
            elif not self.onwakeup:
                data.state = lv.INDEV_STATE.PRESSED
        else:
            self.onwakeup = False
            data.state = lv.INDEV_STATE.RELEASED
        data.key = lv.KEY.ESC