import time

from machine import PWM

from . import Device
from ..task_scheduler import Task, TASKEXIT

# 蜂鸣器驱动

class Buzzer(Device):
    def __init__(self, buzzer_pin):
        self.buzzer_pin = buzzer_pin
        self.buzzer = PWM(self.buzzer_pin)
        self.beep_task = Task(self.beep_task_func, 100)
        self.freq_list = []
        self.volume = 100

    def set_volume(self, volume):
        # 设置音量，有效值 0-100
        if volume <= 0:
            self.volume = 0
        elif volume >= 100:
            self.volume = 100
        else:
            self.volume = volume

    def stop_pwm(self):
        # 停止整个 PWM
        self.buzzer.duty_u16(0)
        time.sleep_ms(2)
        self.buzzer.deinit()

    def beep(self, freq=4000):
        # 滴一声，可选参数为频率
        if len(self.freq_list) == 0:
            self.freq_list.append(freq)
            self.beep_task.start()
            return True
        return False

    def play(self, freqs):
        # 播放一段频率列表
        if len(self.freq_list) == 0:
            self.freq_list.extend(freqs)
            self.beep_task.start()
            return True
        return False

    def stop(self):
        # 停止播放
        self.freq_list.clear()

    def beep_task_func(self):
        if len(self.freq_list) == 0:
            self.stop_pwm()
            return TASKEXIT
        freq = self.freq_list.pop(0)
        if freq == 0:
            self.buzzer.duty_u16(0)
        else:
            self.buzzer.freq(freq)
            self.buzzer.duty_u16(self.volume * 300)

