from machine import ADC

from . import Device

_VFULL = 4.2
_VEMPTY = 3.3

class Battery(Device):
    def __init__(self, bat_pin):
        self.bat_pin = bat_pin
        self.bat_adc = ADC(self.bat_pin)

    def voltage(self):
        return (self.bat_adc.read_u16() * 3.3 * 3) / 65535

    def micro_voltage(self):
        # 粗略计算
        return (self.bad_adc.read_u16() * 3300 * 3) >> 16

    def level(self):
        return int(10 * (self.voltage() - _VEMPTY) / (_VFULL - _VEMPTY)) * 10


