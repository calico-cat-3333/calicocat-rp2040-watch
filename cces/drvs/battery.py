from machine import ADC
from micropython import const

from . import Device

# 电池驱动
# 很显然，直接用 ADC 读电池电压的方法来判断电池容量和状态准度非常差
# 但是没办法，成本限制在这了

_MVFULL = const(4000)
_MVEMPTY = const(3300)
_MVCHARGE = const(4100)
_MVCHARGE_DONE = const(4300)
_ADC_DIVISOR = const(3)
_U16FULL = int((_MVFULL * 65535) / (_ADC_DIVISOR * 3300))
_U16EMPTY = int((_MVEMPTY * 65535) / (_ADC_DIVISOR * 3300))
_U16CHARGE = int((_MVCHARGE * 65535) / (_ADC_DIVISOR * 3300))
# _U16CHARGE_DONE = int((_MVCHARGE_DONE * 65535) / (_ADC_DIVISOR * 3300))

class Battery(Device):
    def __init__(self, bat_pin):
        self.bat_pin = bat_pin
        self.bat_adc = ADC(self.bat_pin)

    def _volt(self, u16):
        return (u16 * 3.3 * _ADC_DIVISOR) / 65535

    def _mvolt(self, u16):
        return (u16 * 3300 * _ADC_DIVISOR) >> 16

    def _ischarge(self, u16):
        if u16 > _U16CHARGE:
            return True
        return False

    def _level(self, u16):
        if u16 > _U16CHARGE:
            return 90
        if u16 > _U16FULL:
            return 100
        if u16 < _U16EMPTY:
            return 0
        return int(10 * (u16 - _U16EMPTY) / (_U16FULL - _U16EMPTY)) * 10

    def voltage(self):
        # 计算电压，返回浮点数
        return self._volt(self.bat_adc.read_u16())

    def micro_voltage(self):
        # 粗略计算毫伏值，返回整数
        return self._mvolt(self.bat_adc.read_u16())

    def level(self):
        # 返回粗略估计的电量
        return self._level(self.bat_adc.read_u16())

    def charging(self):
        # 猜测充电状态
        return self._ischarge(self.bat_adc.read_u16())

    def dump(self):
        # 一次性读取全部状态
        v = self.bat_adc.read_u16()
        return (self._volt(v), self._mvolt(v), self._level(v), self._ischarge(v), v)