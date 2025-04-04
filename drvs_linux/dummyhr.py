from .device import Device
# 假装这里有心率传感器
from cces.log import log
from cces.task_scheduler import Task

import time
import math
import struct

from micropython import const
from collections import deque

# 假装这里有心率传感器
_RESULT_TIMEOUT = const(300) # 测量结果有效期
_WINDOW_SIZE = const(5) # 滑动窗口大小
_BUFFER_SIZE = const(50)

class HRM(Device):
    def __init__(self):
        time.sleep_ms(10)
        self.red_buf = deque((), _BUFFER_SIZE)
        self.red_sw = deque((), _WINDOW_SIZE)
        self.ir_buf = deque((), _BUFFER_SIZE)
        self.ir_sw = deque((), _WINDOW_SIZE)
        self.config()
        self.shutdown()
        self.read_task = Task(self.fifo_smoothread, 1000)

    def config(self, sample_average=8, sample_rate=100, led_power=0x7F):
        # apply default config
        # 出于减小程序体积因素考虑，这里仅提供少量配置的能力
        # sample_average : 1,2,4,8,16,32
        # sample_rate: 50, 100, 200, 400, 800 do not set to 1000, 1600, 3200
        # adc_range: 0-2048, 1-4096, 2-8192, 3-16384
        self.reset()
        # set FIFO sample avgrage, enable fifo rollover
        self.sample_average = sample_average
        log('set fifo config', bin((int(math.log(sample_average, 2)) << 5) | 0x1f))
        self.sample_rate = sample_rate # (int(math.log(sample_rate / 50, 2)) << 2)
        self.data_rate = sample_rate / sample_average
        log('set mode config', bin((int(math.log(sample_rate / 50, 2)) << 2) | 0x63))
        self.fifo_clear()
        self.dhr = -1
        self.dspo2 = -1

    def reset(self):
        self.buf_clear()

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
        log('hrm fifo clear')

    def shutdown(self):
        log('hrm shutdonw')

    def wakeup(self):
        log('hrm wakeup')

    def part_id(self):
        return 0

    def revision_id(self):
        return 0

    def read_temperature(self):
        return 0.0

    def fifo_read(self):
        pass

    def fifo_smoothread(self):
        # 使用滑动窗口平均化处理后再放入 buf
        log('fifo smoothread')

    def buf_any(self):
        return len(self.red_buf)

    def buf_pop(self):
        return self.red_buf.popleft(), self.ir_buf.popleft()

    def calculate_hr(self):
        return self.dhr

    def calculate_spo2(self):
        return self.dspo2

    def start_measure(self):
        self.wakeup()
        self.buf_clear()
        self.sw_clear()
        self.read_task.start()
        self.dhr = 80
        self.dspo2 = 98

    def stop_measure(self):
        self.read_task.stop()
        self.shutdown()
        self.buf_clear()
        self.sw_clear()
        self.dhr = -1
        self.dspo2 = -1
