import time
import struct

from micropython import const

from . import Device

_QMI8658_Address = const(0x6B)

# QMI8658_Register
_QMI8658_WHO_AM_I = const(0x00)
_QMI8658_REVISION_ID = const(0x01)

_QMI8658_CTRL1 = const(0x02)
_QMI8658_CTRL2 = const(0x03)
_QMI8658_CTRL3 = const(0x04)
_QMI8658_CTRL4 = const(0x05) # Reserved in datasheet
_QMI8658_CTRL5 = const(0x06)
_QMI8658_CTRL6 = const(0x07) # Reserved in datasheet
_QMI8658_CTRL7 = const(0x08)
_QMI8658_CTRL8 = const(0x09)
_QMI8658_CTRL9 = const(0x0A)

_QMI8658_CAL1_L = const(0x0B)
_QMI8658_CAL1_H = const(0x0C)
_QMI8658_CAL2_L = const(0x0D)
_QMI8658_CAL2_H = const(0x0E)
_QMI8658_CAL3_L = const(0x0F)
_QMI8658_CAL3_H = const(0x10)
_QMI8658_CAL4_L = const(0x11)
_QMI8658_CAL4_H = const(0x12)

_QMI8658_FIFO_WTM_TH = const(0x13)
_QMI8658_FIFO_CTRL = const(0x14)
_QMI8658_FIFO_SMPL_CNT = const(0x15)
_QMI8658_FIFO_STATUS = const(0x16)
_QMI8658_FIFO_DATA = const(0x17)

_QMI8658_STATUSINT = const(0x2D)
_QMI8658_STATUS0 = const(0x2E)
_QMI8658_STATUS1 = const(0x2F)
# 24 bit
_QMI8658_TIMESTAMP_LOW = const(0x30)
_QMI8658_TIMESTAMP_MID = const(0x31)
_QMI8658_TIMESTAMP_HIGH = const(0x32)
# 16 bit
_QMI8658_TEMP_L = const(0x33)
_QMI8658_TEMP_H = const(0x34)
# 16 bit
_QMI8658_AX_L = const(0x35)
_QMI8658_AX_H = const(0x36)
_QMI8658_AY_L = const(0x37)
_QMI8658_AY_H = const(0x38)
_QMI8658_AZ_L = const(0x39)
_QMI8658_AZ_H = const(0x3A)
# 16 bit
_QMI8658_GX_L = const(0x3B)
_QMI8658_GX_H = const(0x3C)
_QMI8658_GY_L = const(0x3D)
_QMI8658_GY_H = const(0x3E)
_QMI8658_GZ_L = const(0x3F)
_QMI8658_GZ_H = const(0x40)

_QMI8658_COD_STATUS = const(0x46)

_QMI8658_TAP_STATUS = const(0x59)
# 24 bit
_QMI8658_STEP_CNT_LOW = const(0x5A)
_QMI8658_STEP_CNT_MID = const(0x5B)
_QMI8658_STEP_CNT_HIGH = const(0x5C)

_QMI8658_RESET = const(0x60)

# CTRL9 cmd list
CTRL9_CMD_ACK = const(0x00)  # Acknowledgement to end the protocol
CTRL9_CMD_RST_FIFO = const(0x04)  # Reset FIFO from Host
CTRL9_CMD_REQ_FIFO = const(0x05)  # Get FIFO data from Device
CTRL9_CMD_WRITE_WOM_SETTING = const(0x08)  # Set up and enable Wake on Motion (WoM)
CTRL9_CMD_ACCEL_HOST_DELTA_OFFSET = const(0x09)  # Change accelerometer offset
CTRL9_CMD_GYRO_HOST_DELTA_OFFSET = const(0x0A)  # Change gyroscope offset
CTRL9_CMD_CONFIGURE_TAP = const(0x0C)  # Configure Tap detection
CTRL9_CMD_CONFIGURE_PEDOMETER = const(0x0D)  # Configure Pedometer
CTRL9_CMD_CONFIGURE_MOTION = const(0x0E)  # Configure Any Motion / No Motion / Significant Motion detection
CTRL9_CMD_RESET_PEDOMETER = const(0x0F)  # Reset pedometer count (step count)
CTRL9_CMD_COPY_USID = const(0x10)  # Copy USID and FW Version to UI registers
CTRL9_CMD_SET_RPU = const(0x11)  # Configures IO pull-ups
CTRL9_CMD_AHB_CLOCK_GATING = const(0x12)  # Internal AHB clock gating switch
CTRL9_CMD_ON_DEMAND_CALIBRATION = const(0xA2)  # On-Demand Calibration on gyroscope
CTRL9_CMD_APPLY_GYRO_GAINS = const(0xAA)  # Restore the saved Gyroscope gains

# Accelerometer Full Size
_ACC_RANGE_2G = const(1 << 14)
_ACC_RANGE_4G = const(1 << 13)
_ACC_RANGE_8G = const(1 << 12)
_ACC_RANGE_16G = const(1 << 11)

# Gyroscope Full Size
_GYR_RANGE_16DPS = const(1 << 11)
_GYR_RANGE_32DPS = const(1 << 10)
_GYR_RANGE_64DPS = const(1 << 9)
_GYR_RANGE_128DPS = const(1 << 8)
_GYR_RANGE_256DPS = const(1 << 7)
_GYR_RANGE_512DPS = const(1 << 6)
_GYR_RANGE_1024DPS = const(1 << 5)
_GYR_RANGE_2048DPS = const(1 << 4)

class QMI8658(Device):
    def __init__(self, i2c, *, int1=None, int2=None, use_fifo=False, address=_QMI8658_Address):
        self.i2c = i2c
        self.int1 = int1 # motion event interrupt
        self.int2 = int2 # data ready or fifo interrupt
        self.use_fifo = use_fifo # FIFO not work, disable by default
        self.address = address
        time.sleep_ms(5)

        whoami, rev = self.chip_info()
        if whoami != 0x05:
            print('not a QMI8658')

        self.reset()
        self.config()

    def i2c_write(self, reg, data):
        self.i2c.writeto_mem(self.address, reg, bytes([data]))

    def i2c_read(self, reg, length=1):
        data = bytearray(length)
        self.i2c.readfrom_mem_into(self.address, reg, data)
        return data

    def i2c_read16(self, reg, length=1):
        # read 2 bytes as low high bytes from reg, then convert to int16 type
        data = self.i2c_read(reg, 2 * length)
        fmt = '<' + ('h' * length)
        return struct.unpack(fmt, data)

    def i2c_read24(self, reg):
        # read 3 bytes as low mid high bytes from reg
        data = self.i2c_read(reg, 3)
        return (data[2] << 16) + (data[1] << 8) + data[0]

    def config(self):
        # default config
        self.i2c_write(_QMI8658_CTRL1, 0x78) # enable int1 and int2
        self.i2c_write(_QMI8658_CTRL2, 0x05) # Accelerometer Full-scale = ±2 g, ODR Rate 224.2 Hz
        self.accel_fs_div = _ACC_RANGE_2G
        self.accel_odr = 224.2
        self.i2c_write(_QMI8658_CTRL3, 0x55) # Gyroscope Full-scale ±512 dps, ODR Rate 224.2 Hz
        self.gyro_fs_div = _GYR_RANGE_512DPS
        self.gyro_odr = 224.2
        self.i2c_write(_QMI8658_CTRL4, 0x00) # No use
        self.i2c_write(_QMI8658_CTRL5, 0x11) # Enable Accelerometer and Gyroscope Low-Pass Filter whth BW: 2.66% of ODR (Hz)
        self.i2c_write(_QMI8658_CTRL6, 0x00) # No use
        self.i2c_write(_QMI8658_CTRL8, 0xD0) # Enable Pedometer, use STATUSINT.bit7 as CTRL9 handshake, map motion events interrupt to int1

        if self.use_fifo:
            self.ctrl9w_cmd(CTRL9_CMD_RST_FIFO)
            self.i2c_write(_QMI8658_FIFO_CTRL, 0x03) # FIFO sample size 128, mode FIFO
            self.i2c_write(_QMI8658_FIFO_WTM_TH, 16) # 16 sample trigger fifo watermark

        self.config_pedometer()

        self.i2c_write(_QMI8658_CTRL7, 0x03) # Enable Accelerometer and Gyroscope

    def reset(self):
        # soft reset
        self.i2c_write(_QMI8658_RESET, 0xB0)
        time.sleep_ms(15)
        if self.i2c_read(0x4D)[0] == 0x80:
            return True
        return False

    def chip_info(self):
        # return chip id and revision id
        return self.i2c_read(_QMI8658_WHO_AM_I)[0], self.i2c_read(_QMI8658_REVISION_ID)[0]

    def ctrl9_cmddone(self):
        return (self.i2c_read(_QMI8658_STATUSINT)[0] & 0x80) >> 7

    def ctrl9_cmd(self, cmd):
        self.i2c_write(_QMI8658_CTRL9, cmd)

    def ctrl9_ack(self):
        self.i2c_write(_QMI8658_CTRL9, CTRL9_CMD_ACK)
        while self.ctrl9_cmddone():
            time.sleep_ms(1)

    def ctrl9w_cmd(self, cmd):
        self.ctrl9_cmd(cmd)
        while not self.ctrl9_cmddone():
            time.sleep_ms(1)
        self.ctrl9_ack()

    def int16_conv(self, data):
        # 将 16 位二进制补码转换为整形
        # unused
        if data > 32767:
            return data - 0xFFFF + 1
        return data

    def int8_conv(self, data):
        # 将 8 位二进制补码转换为整形
        if data > 127:
            return data - 0xFF + 1
        return data

    def get_dataready(self):
        return self.int2.value()

    def get_gyro_xyz(self):
        if (not self.use_fifo) and (not self.int2.value()):
            return None
        xyz = list(self.i2c_read16(_QMI8658_GX_L, 3))
        for i in range(3):
            xyz[i] = xyz[i] / self.gyro_fs_div
        return xyz

    def get_accel_xyz(self):
        if (not self.use_fifo) and (not self.int2.value()):
            return None
        xyz = list(self.i2c_read16(_QMI8658_AX_L, 3))
        for i in range(3):
            xyz[i] = xyz[i] / self.accel_fs_div
        return xyz

    def get_timestamp(self):
        return self.i2c_read24(_QMI8658_TIMESTAMP_LOW)

    def get_temperature(self):
        raw_data = self.i2c_read(_QMI8658_TEMP_L, 2)
        return self.int8_conv(raw_data[1]) + (self.int8_conv(raw_data[0]) / 256.0)

    def config_pedometer(self,
                         sample_cnt=225,
                         fix_peek2peek=0x00CC,
                         fix_peek=0x0066,
                         time_up_ms=4000,
                         time_low_ms=450,
                         time_cnt_entry=5,
                         fix_precision=0,
                         sig_count=5):
        # must done before enable accel and gyro
        self.i2c_write(_QMI8658_CAL1_L, sample_cnt & 0xff)
        self.i2c_write(_QMI8658_CAL1_H, (sample_cnt >> 8) & 0xff)
        self.i2c_write(_QMI8658_CAL2_L, fix_peek2peek & 0xff)
        self.i2c_write(_QMI8658_CAL2_H, (fix_peek2peek >> 8) & 0xff)
        self.i2c_write(_QMI8658_CAL3_L, fix_peek & 0xff)
        self.i2c_write(_QMI8658_CAL3_H, (fix_peek >> 8) & 0xff)
        self.i2c_write(_QMI8658_CAL4_L, 0x00)
        self.i2c_write(_QMI8658_CAL4_H, 0x01)

        self.ctrl9w_cmd(CTRL9_CMD_CONFIGURE_PEDOMETER)

        time_up = int((time_up_ms * self.accel_odr) / 1000)
        time_low = int((time_low_ms * self.accel_odr) / 1000)

        self.i2c_write(_QMI8658_CAL1_L, time_up & 0xff)
        self.i2c_write(_QMI8658_CAL1_H, (time_up >> 8) & 0xff)
        self.i2c_write(_QMI8658_CAL2_L, time_low & 0xff)
        self.i2c_write(_QMI8658_CAL2_H, time_cnt_entry & 0xff)
        self.i2c_write(_QMI8658_CAL3_L, fix_precision & 0xff)
        self.i2c_write(_QMI8658_CAL3_H, sig_count & 0xff)
        self.i2c_write(_QMI8658_CAL4_L, 0x00)
        self.i2c_write(_QMI8658_CAL4_H, 0x02)

        self.ctrl9w_cmd(CTRL9_CMD_CONFIGURE_PEDOMETER)

    def get_step(self):
        return self.i2c_read24(_QMI8658_STEP_CNT_LOW)

    def clear_step(self):
        self.ctrl9w_cmd(CTRL9_CMD_RESET_PEDOMETER)

    def is_fifo_full(self):
        return (self.i2c_read(_QMI8658_FIFO_STATUS)[0] & 0x80) >> 7

    def is_fifo_wtm(self):
        return (self.i2c_read(_QMI8658_FIFO_STATUS)[0] & 0x40) >> 6

    def get_fifo_sample_size(self):
        return ((self.i2c_read(_QMI8658_FIFO_STATUS)[0] & 0x03) << 8) + self.i2c_read(_QMI8658_FIFO_SMPL_CNT)[0]

    def read_fifo_raw(self):
        sample_size = self.get_fifo_sample_size()
        self.ctrl9w_cmd(CTRL9_CMD_REQ_FIFO)
        data = self.i2c_read(_QMI8658_FIFO_DATA, sample_size * 2)
        self.i2c_write(_QMI8658_FIFO_CTRL, 0x03)
        return data, sample_size * 2

    def read_fifo(self):
        sample_size = self.get_fifo_sample_size()
        self.ctrl9w_cmd(CTRL9_CMD_REQ_FIFO)
        data = self.i2c_read16(_QMI8658_FIFO_DATA, self.get_fifo_sample_size())
        self.i2c_write(_QMI8658_FIFO_CTRL, 0x03)
        accel_data = []
        gyro_data = []
        for i in range(int(sample_size / 6)):
            accel_data.append([data[0 + i * 6], data[1 + i * 6], data[2 + i * 6]])
            gyro_data.append([data[3 + i * 6], data[4 + i * 6], data[5 + i * 6]])
        return accel_data, gyro_data, int(sample_size / 6)