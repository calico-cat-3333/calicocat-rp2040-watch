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
        return (self.bat_adc.read_u16() * 3.3 * 3) / 65535

    def micro_voltage(self):
        # 粗略计算
        return (self.bat_adc.read_u16() * 3300 * 3) >> 16

    def level(self):
        v = self.voltage()
        if v > _VFULL:
            return 100
        if v < _VEMPTY:
            return 0
        return int(10 * (v - _VEMPTY) / (_VFULL - _VEMPTY)) * 10

    def charging(self):
        if self.micro_voltage() >= _MVCHARG:
            return True
        else:
            return False