from cces import system
from cces.drvs import e104ble, battery, buzzer, rtc
from cces.drvs import cst816s_lv, gc9a01_lv, qmi8658, Device
from cces import hal
from cces import log

import board
import extboard

log.setlevel(log.INFO)

hal.dispdev = gc9a01_lv.GC9A01_lv(board.lcd_spi, board.lcd_rst, board.lcd_cs, board.lcd_dc, board.lcd_bl)
hal.indev_list.append(cst816s_lv.CST816S_lv(board.i2c1, board.tp_int, board.tp_rst))

hal.rtc = rtc.RTC()
hal.buzzer = buzzer.Buzzer(extboard.buzzer_pin)
hal.imu = qmi8658.QMI8658(board.i2c1, int1=board.imu_int1, int2=board.imu_int2)
hal.hartrate = Device()
hal.battery = battery.Battery(board.bat_pin)
hal.ble = e104ble.E104BLE(extboard.rx, extboard.tx, extboard.si2c)

system.start()