from machine import ADC

from . import Device

_VFULL = 4.2
_VEMPTY = 3.3
_MVCHARG = 4200

class Battery(Device):
    def __init__(self, bat_pin):
        self.bat_pin = bat_pin
        self.bat_adc = ADC(self.bat_pin)

    def voltage(self):
        # 计算电压，返回浮点数
        return (self.bat_adc.read_u16() * 3.3 * 3) / 65535

    def micro_voltage(self):
        # 粗略计算毫伏值，返回整数
        return (self.bat_adc.read_u16() * 3300 * 3) >> 16

    def level(self):
        # 粗略估计容量，返回值范围 0-100
        v = self.voltage()
        if v > _VFULL:
            return 100
        if v < _VEMPTY:
            return 0
        return int(10 * (v - _VEMPTY) / (_VFULL - _VEMPTY)) * 10

    def charging(self):
        # 判断是否在充电，大概不算很准
        if self.micro_voltage() >= _MVCHARG:
            return True
        else:
            return False