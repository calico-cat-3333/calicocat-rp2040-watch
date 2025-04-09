import lvgl as lv
import time

from cces.appmgr import AppMeta
from cces.activity import Activity, fonts
from cces.task_scheduler import Task
from cces import hal

running_timer = -1 # 是 -1 或者 time.time()
timer_stop = -1 # 是 -1 或者 time.time()

class MainActivity(Activity):
    def __init__(self):
        self.update_display_task = Task(self.update_display, 1000)

    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.start_btn = lv.button(self.scr)
        self.start_btn.set_size(70, 70)
        self.start_btn.align(lv.ALIGN.BOTTOM_MID, 0, -20)
        self.start_btn.set_style_radius(70, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.start_btn.add_event_cb(self.start_btn_cb, lv.EVENT.CLICKED, None)

        self.btn_label = lv.label(self.start_btn)
        self.btn_label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn_label.align(lv.ALIGN.CENTER, 0, 0)

        self.time_label = lv.label(self.scr)
        self.time_label.align(lv.ALIGN.CENTER, 0, -20)
        self.time_label.set_style_text_font(lv.font_number72, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.title_label = lv.label(self.scr)
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 10)
        self.title_label.set_text('计时器')

        if running_timer != -1 and timer_stop == -1:
            self.update_display_task.start()

        self.update_display()

    def update_display(self):
        if running_timer == -1: # not started
            td = 0
            self.btn_label.set_text(lv.SYMBOL.PLAY)
        elif timer_stop != -1: # stopped
            td = timer_stop - running_timer
            self.btn_label.set_text(lv.SYMBOL.REFRESH)
        else: # running
            td = int(time.time() - running_timer)
            self.btn_label.set_text(lv.SYMBOL.STOP)
        s = td % 60
        m = (td // 60) % 60
        h = (td // 3600)
        self.time_label.set_text('{:d}:{:0>2d}:{:0>2d}'.format(h, m, s))

    def start_btn_cb(self, _):
        global running_timer
        global timer_stop
        if running_timer == -1: # start
            running_timer = int(time.time())
            timer_stop = -1
            #self.btn_label.set_text(lv.SYMBOL.STOP)
            self.update_display_task.start()
        elif timer_stop != -1: # reset
            timer_stop = -1
            running_timer = -1
            self.update_display()
            #self.btn_label.set_text(lv.SYMBOL.PLAY)
        else: # stop
            timer_stop = int(time.time())
            #self.btn_label.set_text(lv.SYMBOL.REFRESH)
            self.update_display_task.stop()
            self.update_display()
        hal.buzzer.beep()

    def before_exit(self):
        self.update_display_task.stop()

    def on_cover_exit(self):
        if running_timer != -1 and timer_stop == -1:
            self.update_display_task.start()
        self.update_display()

    def on_covered(self):
        self.update_display_task.stop()

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.RIGHT:
            self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

appmeta = AppMeta('计时器', fonts.SYMBOL.STOPWATCH, MainActivity)