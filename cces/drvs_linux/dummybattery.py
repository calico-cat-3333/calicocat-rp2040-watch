from micropython import const

from . import Device

# 假装这里有电池

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
    def __init__(self, fake_adc_value=25000):
        self.fake_adc_value = fake_adc_value

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
        return self._volt(self.fake_adc_value)

    def micro_voltage(self):
        # 粗略计算毫伏值，返回整数
        return self._mvolt(self.fake_adc_value)

    def level(self):
        # 返回粗略估计的电量
        return self._level(self.fake_adc_value)

    def charging(self):
        # 猜测充电状态
        return self._ischarge(self.fake_adc_value)

    def dump(self):
        # 一次性读取全部状态
        v = self.fake_adc_value
        return (self._volt(v), self._mvolt(v), self._level(v), self._ischarge(v), v)