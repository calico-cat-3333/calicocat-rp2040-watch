from .activity import Activity
from .activity.askyesno import AskYesNoActivity
from .task_scheduler import Task

import lvgl as lv

import time
import gc
from . import hal

class WatchFaceAtivity(Activity):
    def __init__(self):
        self.update_display_task = Task(self.update_display, 1000) # update display every 10 secs
        self.number_font = lv.binfont_create("S:number_72.bin")

    def setup(self):
        self.scr.add_event_cb(self.gesture_event_handler, lv.EVENT.GESTURE, None)
        self.date_label = lv.label(self.scr)
        self.date_label.align(lv.ALIGN.CENTER, 0, -60)
        self.date_label.set_text('YYYY-MM-DD')

        self.time_label = lv.label(self.scr)
        self.time_label.align(lv.ALIGN.CENTER, 0, 0)
        self.time_label.set_style_text_font(self.number_font, 0)
        self.time_label.set_text('--:--:--')

        self.bat_label = lv.label(self.scr)
        self.bat_label.align(lv.ALIGN.BOTTOM_MID, 0, -10)
        self.bat_label.set_text('BBB%')

        self.step_label = lv.label(self.scr)
        self.step_label.align(lv.ALIGN.CENTER, -50, 60)
        self.step_label.set_text('steps:--')

        self.update_display_task.start()

    def on_covered(self):
        self.update_display_task.stop()

    def on_cover_exit(self):
        self.update_display_task.start()

    def update_display(self):
        lt = time.localtime()
        self.date_label.set_text('{:0>4d}-{:0>2d}-{:0>2d}'.format(*lt[:3]))
        self.time_label.set_text('{:0>2d}:{:0>2d}:{:0>2d}'.format(*lt[3:6]))
        #self.bat_label.set_text('{:>3d}%'.format(hal.battery.level()))
        self.step_label.set_text('steps:{:d}'.format(hal.imu.get_step()))

    def infookclick(self):
        print(2222)

    def noclickcb(self):
        hal.buzzer.beep()

    def gesture_event_handler(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.TOP:
            AskYesNoActivity('MemoryFree', 'Mem Free: '+str(gc.mem_free()), self.infookclick, self.noclickcb).launch()

