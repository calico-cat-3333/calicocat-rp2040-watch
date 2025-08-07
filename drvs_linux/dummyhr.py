from cces.drvs import Device
# 假装这里有心率传感器
from cces.log import log
from cces.task_scheduler import Task

import time
import math
import struct
from random import randint

from micropython import const

# 假装这里有心率传感器

class HRM(Device):
    def __init__(self):
        time.sleep_ms(10)
        self.config()
        self.shutdown()
        self.read_task = Task(self.fifo_smoothread, 1000)

    def config(self):
        self.reset()
        self.fifo_clear()
        self.dhr = -1
        self.dspo2 = -1

    def reset(self):
        log('dummyhr: reset')

    def fifo_clear(self):
        log('dummyhr fifo clear')

    def shutdown(self):
        log('dummyhr shutdonw')

    def wakeup(self):
        log('dummyhr wakeup')

    def part_id(self):
        return 0

    def revision_id(self):
        return 0

    def read_temperature(self):
        return 0.0

    def fifo_read(self):
        log('dummyhr: fifo read')
        self.dhr = randint(60, 180)
        self.dspo2 = randint(80, 100)

    def fifo_smoothread(self):
        # 使用滑动窗口平均化处理后再放入 buf
        log('dummyhr: fifo smoothread')
        self.dhr = randint(60, 180)
        self.dspo2 = randint(80, 100)

    def buf_any(self):
        return 1

    def buf_pop(self):
        return 1, 1

    def calculate_hr(self):
        return self.dhr

    def calculate_spo2(self):
        return self.dspo2

    def start_measure(self):
        self.wakeup()
        self.read_task.start()

    def stop_measure(self):
        self.read_task.stop()
        self.shutdown()
        self.dhr = -1
        self.dspo2 = -1
