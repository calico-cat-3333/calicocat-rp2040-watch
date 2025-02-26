# 硬件抽象层
# 对上层应用提供统一的硬件访问方式。

class Device:
    def on_wakeup(self):
        pass

    def on_sleep(self):
        pass

class Device_lv(Device):
    def after_lvgl_init(self):
        pass

imu = None
indev_list = []
screen = None
hartrate = None
buzzer = None

def after_lvgl_init():
    if screen == None or len(indev_list) == 0:
        print('Error: driver not set')
        return
    screen.after_lvgl_init()
    for dev in indev_list:
        dev.after_lvgl_init()
