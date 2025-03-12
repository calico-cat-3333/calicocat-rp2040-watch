# 硬件抽象层
# 对上层应用提供统一的硬件访问方式。

from machine import RTC

class Device:
    def on_wakeup(self):
        pass

    def on_sleep(self):
        pass

class Device_lv(Device):
    def after_lvgl_init(self):
        raise NotImplementedError('after_lvgl_init() not implemented')

rtc = RTC()
# rtc for set time only
# use rtc.datetime((y,m,d,0,h,m,s,0)) to set time

imu = None
# imu should have:
# get_step
# clear_step
# get_accel_xyz
# get_gyro_xyz

indev_list = []
# lvgl input devices

dispdev = None
# lvgl display_device, should also have:
# brightness

hartrate = None
# hartrate should have:

buzzer = None
# buzzer should have:
# beep

battery = None
# battery should have:
# chargeing
# level
# voltage

ble = None
# ble uart device should have
# uart_rxs
# uart_tx


def after_lvgl_init():
    if dispdev == None or len(indev_list) == 0:
        print('Error: driver not set')
        return
    dispdev.after_lvgl_init()
    for indev in indev_list:
        indev.after_lvgl_init()

def on_sleep():
    dispdev.on_sleep()
    for indev in indev_list:
        indev.on_sleep()
    hartrate.on_sleep()
    imu.on_sleep()
    buzzer.on_sleep()
    battery.on_sleep()
    ble.on_sleep()

def on_wakeup():
    dispdev.on_wakeup()
    for indev in indev_list:
        indev.on_wakeup()
    hartrate.on_wakeup()
    imu.on_wakeup()
    buzzer.on_wakeup()
    battery.on_wakeup()
    ble.on_wakeup()