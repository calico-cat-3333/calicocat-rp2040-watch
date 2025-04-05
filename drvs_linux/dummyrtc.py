from cces.log import log
import time

class RTC:
    def __init__(self):
        pass

    def set_time_unix(self, timestamp):
        log('dummyrtc: set time to:', time.localtime(timestamp))

    def set_time(y, m, d, h, mm, s):
        log('dummyrtc: set time to:', y, m, d, h, mm, s)
