class Device:
    def on_wakeup(self):
        # 设备从休眠中唤醒时执行
        pass

    def on_sleep(self):
        # 设备休眠时执行
        pass

class Device_lv(Device):
    def after_lvgl_init(self):
        # lvgl 初始化完成后执行，对于直接对接 lvgl 的设备，这个函数是必须的
        # lvgl 相关的初始化不能再 __init__ 函数中编写，必须写在这里
        raise NotImplementedError('after_lvgl_init() not implemented')