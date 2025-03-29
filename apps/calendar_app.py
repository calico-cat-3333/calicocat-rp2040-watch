import lvgl as lv
import time

from cces.appmgr import AppMeta
from cces.activity import Activity, REFRESHON

class MainActivity(Activity):
    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.refresh_on = self.refresh_on | REFRESHON.ZERO_CLOCK

        self.header_label = lv.label(self.scr)
        self.header_label.align(lv.ALIGN.TOP_MID, 0, 5)

        self.cal = lv.calendar(self.scr)
        self.cal.align(lv.ALIGN.CENTER, 0, 5)
        self.cal.set_size(210, 200)
        self.cal.set_style_text_font(lv.font_chinese_calendar, 0)
        self.cal.set_style_border_side(lv.BORDER_SIDE.NONE, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cal.set_chinese_mode(True)
        self.update_display(True)

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.RIGHT:
            self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)
        elif gesture == lv.DIR.TOP:
            self.shown_month[0] = self.shown_month[0] + (self.shown_month[1]) // 12
            self.shown_month[1] = (self.shown_month[1]) % 12 + 1
            self.update_display()
        elif gesture == lv.DIR.BOTTOM:
            self.shown_month[0] = self.shown_month[0] + (self.shown_month[1] - 2) // 12
            self.shown_month[1] = (self.shown_month[1] - 2) % 12 + 1
            self.update_display()
        elif gesture == lv.DIR.LEFT:
            self.update_display(True)

    def update_display(self, return_today=False):
        self.current_date = time.localtime()[:3]
        if return_today:
            self.shown_month = list(self.current_date[:2])
        self.header_label.set_text('{:0>4d}-{:0>2d}'.format(*self.shown_month))
        self.cal.set_today_date(*self.current_date)
        self.cal.set_month_shown(*self.shown_month)

    def refresh_event_cb(self, event):
        self.update_display()

appmeta = AppMeta('日历', lv.SYMBOL.PASTE, MainActivity)