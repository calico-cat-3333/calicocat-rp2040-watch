import time
from machine import RTC as _RTC

class RTC:
    def __init__(self):
        self.rtc = _RTC()

    def set_time_unix(self, timestamp):
        localtime = time.localtime(timestamp)
        self.rtc.datetime((localtime[0], localtime[1], localtime[2], 0, localtime[3], localtime[4], localtime[5], 0))

    def set_time(y,m,d,h,m,s):
        self.rtc.datetime(y, m, d, 0, h, m, s, 0)

    def datetime(self, *args):
        self.rtc.datetime(*args)