# `hal` - 硬件抽象层

统一管理所有硬件，统一硬件接口调用方式。

这里规定了规定硬件接口标准。

这里将这些固定的变量赋值为 None, 在 main.py 中与实际的硬件驱动实例进行关联。

使用时，使用 `hal.设备.函数` 的格式调用。

## rtc

仅用于设置时间，实际包装了 micropython 的 machine.RTC

### set_time_unix(unix)

使用 unix 时间戳设置系统时间。

### set_time(y, m, d, h, m, s)

设置系统时间，参数依次为年，月，日，小时，分钟，秒。

# imu

惯性测量单元。

### get_step()

获取步数。

### clear_step()

清空计步器。

### get_accel_xyz()

获取加速度数据。

### get_gyro_xyz()

获取陀螺仪数据。
### reset()

重置设备。

### config()

应用默认配置，重置后需要调用一次。

# indev_list

LVGL 输入设备列表。

# dispdev

LVGL 显示设备

### set_brightness(birghtness)

设置亮度，范围 0-100

### brightness

当前亮度，只读，应该使用 set_brightness 设置亮度而不是修改这个变量。

# hartrate

PPG 心率血氧传感器。

### shutdown()

关闭。

### wakeup()

开启。

### measure_start()

内置读取任务开始。

### measure_stop()

内置读取任务结束。

### calculate_hr()

获取心率计算结果，如果无法计算返回 -1.

### calculate_spo2()

获取血氧饱和度结果，如果无法计算返回 -1(仅供参考，极不准确)。

### 原始数据接口，一般用不到

### buf_any()

缓冲区中是否有数据，如有，返回数据数量。

### get_buf()

从缓冲区获取数据。

### fifo_read()

将数据读取到缓冲区，需要定期调用。

### fifo_smoothread()

将数据读取到缓冲区并使用滑动窗口进行滤波，需要定期调用。

### reset()

重置。

### config()

重置并应用默认配置。

# buzzer

蜂鸣器。

### beep(freq)

以 freq 频率响 100 毫秒。

### play(freqs=[])

按照列表给出的频率依次播放，每个频率持续 100 毫秒。

### stop()

停止当前播放任务。

### set_volume(volume)

设置音量，范围 0-100.

### volume

读取音量，只读，应该使用 set_volume 设置音量。

# battery

使用 ADC 读取电池电压并判断电量。

### charging()

返回布尔值，表示是否正在充电。

### level()

返回电量等级（%）

### voltage()

返回当前电压（V），浮点数。

### dump()

返回元组：

当前电压（V, 浮点数），当前电压（mV, 整数），电量等级，是否正在充电，ADC 原始读数。

# ble

蓝牙串口设备。

### uart_rx()

从接收缓冲区中取一行数据。

### uart_rx_any()

返回接收缓冲区中的数据数量。

### uart_tx(tx_str)

发送字符串，会自动拼接 "\\r\\n"

### uart_tx_raw(tx_str_raw)

发送字符串。

### reset()

重置。

### connected()

返回是否已连接。

### sleep(mode=None)

查询或设置睡眠模式。

如果参数 mode 为 None 则返回当前睡眠状态，如果 mode 为 True 或 False 则进入或退出睡眠模式。

### sleeping

当前睡眠模式。

只读，不可修改，和 sleep() 函数查询的区别是，这个变量通过读取模块输出中的状态变更字符串变化，可能为 None 即未知睡眠状态，而 sleep() 函数则返回睡眠控制引脚的当前状态。