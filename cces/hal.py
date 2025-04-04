# 硬件抽象层
# 对上层应用提供统一的硬件访问方式。

from .log import log, ERROR
import gc

rtc = None
# rtc for set time only, should have:
# set_time_unix() set time use unix timestamp
# set_time(y,m,d,h,m,s)

imu = None
# imu should have:
# get_step() 获取步数
# clear_step() 清空计步器
# get_accel_xyz() 获取加速度数据
# get_gyro_xyz() 获取陀螺仪数据
# reset() 重置
# config() 应用默认配置，重置后需要调用一次

indev_list = []
# lvgl input devices

dispdev = None
# lvgl display_device, should also have:
# set_brightness(birghtness)
# brightness

hartrate = None
# hartrate should have:
# shutdown() 关闭
# wakeup() 开启
# measure_start() 内置读取任务开始
# measure_stop() 内置读取任务结束
# calculate_hr() 获取心率计算结果，如果无法计算返回 -1
# calculate_spo2() 获取血氧饱和度结果，如果无法计算返回 -1(仅供参考，极不准确)
# 原始数据接口，一般用不到
# buf_any() 缓冲区中是否有数据
# get_buf() 从缓冲区获取数据
# fifo_read() 将数据读取到缓冲区，需要定期调用
# fifo_smoothread() 将数据读取到缓冲区并使用滑动窗口进行滤波，需要定期调用
# reset() 重置
# config() 重置并应用默认配置

buzzer = None
# buzzer should have:
# beep(freq)
# play([freqs])
# stop()
# set_volume(volume)
# volume

battery = None
# battery should have:
# charging()
# level()
# voltage()
# dump()

ble = None
# ble uart device should have
# uart_rx()
# uart_rx_any()
# uart_tx(tx_str)
# uart_tx_raw(tx_str_raw)
# reset()
# connected()
# sleep(mode)
# sleeping


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
    gc.collect()