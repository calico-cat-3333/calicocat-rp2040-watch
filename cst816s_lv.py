import cst816s
import lvgl as lv

class CST816S_lv:
    def __init__(self, i2c, int_pin, rst_pin):
        if not lv.is_initialized():
            lv.init()

        self.tp_drv = cst816s.CST816S(i2c, int_pin, rst_pin)
        self.indev_drv = lv.indev_create()
        self.indev_drv.set_type(lv.INDEV_TYPE.POINTER)
        self.indev_drv.set_read_cb(self.touch_read_cb)

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
