import time
from micropython import const

_CST816_Address = const(0x15)

# CST816S_Register
_CST816_GestureID = const(0x01)
_CST816_FingerNum = const(0x02)
_CST816_XposH = const(0x03)
_CST816_XposL = const(0x04)
_CST816_YposH = const(0x05)
_CST816_YposL = const(0x06)

_CST816_ChipID = const(0xA7)
_CST816_ProjID = const(0xA8)
_CST816_FwVersion = const(0xA9)
_CST816_MotionMask = const(0xAA)

_CST816_BPC0H = const(0xB0)
_CST816_BPC0L = const(0xB1)
_CST816_BPC1H = const(0xB2)
_CST816_BPC1L = const(0xB3)

_CST816_IrqPluseWidth = const(0xED)
_CST816_NorScanPer = const(0xEE)
_CST816_MotionSlAngle = const(0xEF)
_CST816_LpScanRaw1H = const(0XF0)
_CST816_LpScanRaw1L = const(0XF1)
_CST816_LpScanRaw2H = const(0XF2)
_CST816_LpScanRaw2L = const(0XF3)
_CST816_LpAutoWakeTime = const(0XF4)
_CST816_LpScanTH = const(0XF5)
_CST816_LpScanWin = const(0XF6)
_CST816_LpScanFreq = const(0XF7)
_CST816_LpScanIdac = const(0XF8)
_CST816_AutoSleepTime = const(0XF9)
_CST816_IrqCtl = const(0XFA)
_CST816_AutoReset = const(0XFB)
_CST816_LongPressTime = const(0XFC)
_CST816_IOCtl = const(0XFD)
_CST816_DisAutoSleep = const(0XFE)

# CST816S_Mode
_CST816S_Point_Mode = const(1)
_CST816S_Gesture_Mode = const(2)
_CST816S_ALL_Mode = const(3)

# CST816S_Gesture
_CST816S_Gesture_None = const(0)
_CST816S_Gesture_Up = const(1)
_CST816S_Gesture_Down = const(2)
_CST816S_Gesture_Left = const(3)
_CST816S_Gesture_Right = const(4)
_CST816S_Gesture_Click = const(5)
_CST816S_Gesture_Double_Click = const(0x0B)
_CST816S_Gesture_Long_Press = const(0x0C)

class CST816S:
    def __init__(self, i2c, int_pin, rst_pin, *, address=_CST816_Address, sleep=True):
        # int pin and rst pin are required
        # i2c: i2c object, machine.I2C
        # int_pin: interrupt pin, machine.Pin
        # rst_pin: reset pin, machine.Pin
        # address: i2c device address, default 0x15
        # sleep: allow touchpad into sleep mode if no touch in 2 sec, bool, default True
        self.int_pin = int_pin
        self.rst_pin = rst_pin
        self.address = address
        self.reset()
        self.i2c = i2c
        if self.i2c_read(_CST816_ChipID)[0] != 0xB5:
            RuntimeError("Did not find CST816")
        self.set_autosleep(sleep)
        self.set_mode(_CST816S_Point_Mode)

    def i2c_read(self, reg, length=1):
        data = bytearray(length)
        self.i2c.readfrom_mem_into(self.address, reg, data)
        return data

    def i2c_write(self, reg, data):
        self.i2c.writeto_mem(self.address, reg, bytes([data]))

    def reset(self):
        # hard reset
        self.rst_pin.value(0)
        time.sleep_ms(5)
        self.rst_pin.value(1)
        time.sleep_ms(50)

    def read_version(self):
        # read firmware version
        return self.i2c_read(_CST816_FwVersion)[0]

    def set_autosleep(self, mode):
        if mode:
            self.i2c_write(_CST816_DisAutoSleep, 0)
        else:
            self.i2c_write(_CST816_DisAutoSleep, 1)

    def wake_up(self):
        # hard reset and disable autosleep
        self.reset()
        self.set_autosleep(False)

    def set_mode(self, mode):
        if mode == _CST816S_Point_Mode:
            self.i2c_write(_CST816_IrqCtl, 0x41)
            self.mode = mode
        elif mode == _CST816S_Gesture_Mode:
            self.i2c_write(_CST816_IrqCtl, 0x11)
            self.i2c_write(_CST816_MotionMask, 0x01)
            self.mode = mode
        else:
            self.i2c_write(_CST816_IrqCtl, 0x71)
            self.mode = _CST816S_ALL_Mode

    def set_irqplusewidth(self, value):
        if value < 1:
            value = 1
        if value > 200:
            value = 200
        self.i2c_write(_CST816_IrqPluseWidth, value)

    def set_autosleeptime(self, value):
        if value < 1:
            value = 1
        if value > 0xFF:
            value = 0xFF
        self.i2c_write(_CST816_AutoSleepTime, value)

    def get_point(self):
        # get touch point
        touch_data = self.i2c_read(_CST816_XposH, 4)
        xpos = touch_data[1] + ((touch_data[0] & 0x0F) << 8)
        ypos = touch_data[3] + ((touch_data[2] & 0x0F) << 8)
        return xpos, ypos

    def get_gesture(self):
        gesture = self.i2c_read(_CST816_GestureID)
        return gesture[0]

    def get_fingernum(self):
        fingernum = self.i2c_read(_CST816_FingerNum)
        return fingernum[0]