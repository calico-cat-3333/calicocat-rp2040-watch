from cces import system
from cces.drvs import battery, buzzer, rtc, gpio_button, Device
from cces_drv import cst816s_lv, gc9a01_lv, qmi8658
from cces import hal
from cces import log
from cces import powermanager
import dummyble
import dummyhr

import board
import extboard
import machine

log.setlevel(log.NOLOG)
powermanager.prevent_sleep(True)

hal.dispdev = gc9a01_lv.GC9A01_lv(board.lcd_spi, board.lcd_rst, board.lcd_cs, board.lcd_dc, board.lcd_bl, False, 4)
hal.indev_list.append(cst816s_lv.CST816S_lv(board.i2c1, board.tp_int, board.tp_rst))
hal.indev_list.append(gpio_button.GPIOButton(extboard.btn))

hal.rtc = rtc.RTC()
hal.buzzer = buzzer.Buzzer(extboard.buzzer_pin)
hal.imu = qmi8658.QMI8658(board.i2c1, int1=board.imu_int1, int2=board.imu_int2)
hal.battery = battery.Battery(board.bat_pin)
hal.ble = dummyble.BLE()
hal.hartrate = dummyhr.HRM()

try:
    system.start()
except KeyboardInterrupt as e:
    print(e)
except:
    machine.reset()
