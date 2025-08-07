from cces import system
from drvs_linux import dummyble, dummybattery, dummybuzzer, dummyimu, dummyrtc
from drvs_linux import sdldisp, sdlindev, dummyhr
from cces import hal
from cces import log

log.setlevel(log.INFO)

hal.dispdev = sdldisp.SDLdisp(240, 240)
hal.indev_list.append(sdlindev.SDLindev())

hal.rtc = dummyrtc.RTC()
hal.buzzer = dummybuzzer.Buzzer()
hal.imu = dummyimu.IMU()
hal.hartrate = dummyhr.HRM()
hal.battery = dummybattery.Battery()
hal.ble = dummyble.BLE(True)

system.start()