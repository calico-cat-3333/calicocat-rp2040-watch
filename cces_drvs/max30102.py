import time
import machine
import math
import struct

from micropython import const
from collections import deque

from cces.task_scheduler import Task
from cces.log import log
from cces.drvs import Device

# 心率传感器驱动，内建定长缓冲区，自带滑动窗口平滑算法和心率血氧计算算法

_MAX3010X_I2C_ADDRESS = const(0x57)

_MAX30105_INT_STATUS1 = const(0x00)
_MAX30105_INT_STATUS2 = const(0x01)

_MAX30105_FIFO_WRITE = const(0x04)
_MAX30105_FIFO_OVERFLOW = const(0x05)
_MAX30105_FIFO_READ = const(0x06)
_MAX30105_FIFO_DATA = const(0x07)

_MAX3010X_FIFO_CONFIG = const(0x08)
_MAX3010X_MODE_CONFIG = const(0x09)
_MAX3010X_SPO2_CONFIG = const(0x0A)

_MAX3010X_LED1_PA = const(0x0C)
_MAX3010X_LED2_PA = const(0x0D)
_MAX3010X_PILOT_PA = const(0x10)

_MAX3010X_TEMP_INTEGER = const(0x1F)
_MAX3010X_TEMP_FRACTION = const(0x20)
_MAX3010X_TEMP_CONFIG = const(0x21)

_MAX3010X_REVISION_ID = const(0xFE)
_MAX3010X_PART_ID = const(0xFF)

_RESULT_TIMEOUT = const(300) # 测量结果有效期
_WINDOW_SIZE = const(5) # 滑动窗口大小
_BUFFER_SIZE = const(50)

class MAX30102(Device):
    def __init__(self, i2c, address=_MAX3010X_I2C_ADDRESS):
        self.i2c = i2c
        self.address = address
        time.sleep_ms(10)
        if self.address not in self.i2c.scan():
            print('NOT MAX30102 DEVICE')
        self.red_buf = deque((), _BUFFER_SIZE)
        self.red_sw = deque((), _WINDOW_SIZE)
        self.ir_buf = deque((), _BUFFER_SIZE)
        self.ir_sw = deque((), _WINDOW_SIZE)
        self.config()
        self.shutdown()
        self.read_task = Task(self.fifo_smoothread, 200)

    def config(self, sample_average=8, sample_rate=100, led_power=0x7F):
        # apply default config
        # 出于减小程序体积因素考虑，这里仅提供少量配置的能力
        # sample_average : 1,2,4,8,16,32
        # sample_rate: 50, 100, 200, 400, 800 do not set to 1000, 1600, 3200
        # adc_range: 0-2048, 1-4096, 2-8192, 3-16384
        self.reset()
        # set FIFO sample avgrage, enable fifo rollover
        self.sample_average = sample_average
        self.i2c_write(_MAX3010X_FIFO_CONFIG, (int(math.log(sample_average, 2)) << 5) | 0x1f) # 0b00011111)
        log('set fifo config', bin((int(math.log(sample_average, 2)) << 5) | 0x1f))
        # set to SpO2 mode, with both red and ir led work
        self.i2c_write(_MAX3010X_MODE_CONFIG, 0x03) # 0b00000011)
        # set adc range, sample rate, LED pulse width 411 us
        self.sample_rate = sample_rate # (int(math.log(sample_rate / 50, 2)) << 2)
        self.data_rate = sample_rate / sample_average
        self.i2c_write(_MAX3010X_SPO2_CONFIG, (int(math.log(sample_rate / 50, 2)) << 2) | 0x63)
        log('set mode config', bin((int(math.log(sample_rate / 50, 2)) << 2) | 0x63))
        # set led power
        self.i2c_write(_MAX3010X_LED1_PA, led_power)
        self.i2c_write(_MAX3010X_LED2_PA, led_power)
        self.i2c_write(_MAX3010X_PILOT_PA, led_power)
        self.fifo_clear()

    def reset(self):
        self.buf_clear()
        self.i2c_write(_MAX3010X_MODE_CONFIG, 0b01000000)
        time.sleep_ms(10)
        while bool(self.i2c_read(_MAX3010X_MODE_CONFIG)[0] & 0b01000000):
            time.sleep_ms(10)

    def buf_clear(self):
        for i in range(len(self.red_buf)):
            self.red_buf.pop()
            self.ir_buf.pop()

    def sw_clear(self):
        # 清空滑动窗口
        for i in range(len(self.red_sw)):
            self.red_sw.pop()
            self.ir_sw.pop()

    def fifo_clear(self):
        self.i2c_write(_MAX30105_FIFO_WRITE, 0)
        self.i2c_write(_MAX30105_FIFO_OVERFLOW, 0)
        self.i2c_write(_MAX30105_FIFO_READ, 0)

    def shutdown(self):
        self.i2c_write(_MAX3010X_MODE_CONFIG, 0x83)

    def wakeup(self):
        self.i2c_write(_MAX3010X_MODE_CONFIG, 0x03)

    def part_id(self):
        r = self.i2c_read(_MAX3010X_PART_ID, 1)
        return r[0]

    def revision_id(self):
        r = self.i2c_read(_MAX3010X_REVISION_ID, 1)
        return r[0]

    def read_temperature(self):
        self.i2c_write(_MAX3010X_TEMP_CONFIG, 0x01)
        time.sleep_ms(100)
        while (self.i2c_read(_MAX30105_INT_STATUS2)[0] & 0x02):
            time.sleep_ms(1)
        r = self.i2c_read(_MAX3010X_TEMP_INTEGER, 2)
        return self.int8_conv(r[0]) + r[1] * 0.0625

    def int8_conv(self, data):
        # 将 8 位二进制补码转换为整形
        if data > 127:
            return data - 0xFF + 1
        return data

    def i2c_read(self, reg, length=1):
        data = bytearray(length)
        self.i2c.readfrom_mem_into(self.address, reg, data)
        return data

    def i2c_write(self, reg, data):
        self.i2c.writeto_mem(self.address, reg, bytes([data]))

    def fifo_conv(self, fifo_bytes):
        return (struct.unpack(">i", b'\x00' + fifo_bytes)[0] & 0x3FFFF)

    def fifo_read(self):
        p = self.i2c_read(_MAX30105_FIFO_WRITE, 3)
        wp = p[0] & 0x1f
        rp = p[2] & 0x1f
        if wp == rp:
            return
        sample_num = wp - rp
        if sample_num < 0:
            sample_num = sample_num + 32
        for i in range(sample_num):
            data = self.i2c_read(_MAX30105_FIFO_DATA, 6)
            self.red_buf.append(self.fifo_conv(data[0:3]))
            self.ir_buf.append(self.fifo_conv(data[3:6]))

    def fifo_smoothread(self):
        # 使用滑动窗口平均化处理后再放入 buf
        p = self.i2c_read(_MAX30105_FIFO_WRITE, 3)
        wp = p[0] & 0x1f
        rp = p[2] & 0x1f
        if wp == rp:
            return
        sample_num = wp - rp
        if sample_num < 0:
            sample_num = sample_num + 32
        for i in range(sample_num):
            data = self.i2c_read(_MAX30105_FIFO_DATA, 6)
            self.red_sw.append(self.fifo_conv(data[0:3]))
            self.ir_sw.append(self.fifo_conv(data[3:6]))
            if len(self.red_sw) == _WINDOW_SIZE:
                self.red_buf.append(sum(self.red_sw) // _WINDOW_SIZE)
                self.ir_buf.append(sum(self.ir_sw) // _WINDOW_SIZE)

    def buf_any(self):
        return len(self.red_buf)

    def buf_pop(self):
        return self.red_buf.popleft(), self.ir_buf.popleft()

    def calculate_hr(self):
        if self.buf_any() < _BUFFER_SIZE:
            return -1
        if min(self.ir_buf) < 6000: # 通常意味着未佩戴
            return -1
        peaks = []
        for i in range(1, len(self.ir_buf) - 2):
            if self.ir_buf[i] > self.ir_buf[i - 1] and self.ir_buf[i] >= self.ir_buf[i + 1] and self.ir_buf[i + 1] > self.ir_buf[i + 2]:
                peaks.append(i)
        if len(peaks) < 2:
            return -1
        intervals = [peaks[i + 1] - peaks[i] for i in range(len(peaks) - 1)]
        hr_bpm = (60 * len(intervals) * self.data_rate) / sum(intervals)
        return int(hr_bpm)

    def calculate_spo2(self):
        if self.buf_any() < _BUFFER_SIZE:
            return -1
        if min(self.ir_buf) < 6000: # 通常意味着未佩戴
            return -1
        # 计算 DC 分量（信号均值）
        dc_red = sum(self.red_buf) / len(self.red_buf)
        dc_ir = sum(self.ir_buf) / len(self.ir_buf)
        # 计算 AC 分量（信号最大最小值之差）
        ac_red = max(self.red_buf) - min(self.red_buf)
        ac_ir = max(self.ir_buf) - min(self.ir_buf)
        if ac_ir == 0 or dc_ir == 0 or ac_red == 0 or dc_red == 0:
            return -1  # 防止除零错误
        # 计算 R 值
        R = (ac_red / dc_red) / (ac_ir / dc_ir)
        # 计算 SpO₂
        spo2 = 110 - 25 * R
        # 限制 SpO₂ 范围（一般 90% - 100%）
        spo2 = max(70, min(100, spo2))
        return int(spo2)  # 返回整数值

    def start_measure(self):
        self.wakeup()
        self.buf_clear()
        self.sw_clear()
        self.read_task.start()

    def stop_measure(self):
        self.read_task.stop()
        self.shutdown()
        self.buf_clear()
        self.sw_clear()
