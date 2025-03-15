class Device:
    def on_wakeup(self):
        pass

    def on_sleep(self):
        pass

class Device_lv(Device):
    def after_lvgl_init(self):
        raise NotImplementedError('after_lvgl_init() not implemented')