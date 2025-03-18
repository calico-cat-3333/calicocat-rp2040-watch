# 硬件抽象层
# 对上层应用提供统一的硬件访问方式。

from machine import RTC

from .log import log, ERROR

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
# set_brightness

hartrate = None
# hartrate should have:

buzzer = None
# buzzer should have:
# beep
# play
# stop
# set_volume

battery = None
# battery should have:
# charging
# level
# voltage
# dump

ble = None
# ble uart device should have
# uart_rx
# uart_rx_any
# uart_tx
# uart_rx_raw
# uart_tx_raw


def after_lvgl_init():
    if dispdev == None or len(indev_list) == 0:
        log('lvgl driver not set', level=ERROR)
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