import lvgl as lv
import time
import gc

from .activity import Activity, REFRESHON, fonts
from .activity import QuickSettings
from .task_scheduler import Task
from . import gadgetbridge
from . import hal
from . import settingsdb
from .appmgr import Launcher, launch_app

from .notification import NotificationCenter

_WEEKDAY_NAMES = ('周一', '周二', '周三', '周四', '周五', '周六', '周日')

class WatchFaceAtivity(Activity):
    def __init__(self):
        self.update_display_task = Task(self.update_display, 1000) # update display every 1 secs

    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.refresh_on = REFRESHON.BLE_CONNECTION
        self.sidekey_exit = False
        self.img = lv.image(self.scr)
        self.img.set_src('S:a.png')
        self.img.set_antialias(False)
        self.img.set_scale(512)
        self.img.align(lv.ALIGN.CENTER, 70, 50)
        self.date_label = lv.label(self.scr)
        self.date_label.align(lv.ALIGN.CENTER, 0, -60)
        self.date_label.set_text('YYYY-MM-DD WW')

        self.time_label = lv.label(self.scr)
        self.time_label.align(lv.ALIGN.CENTER, 0, 0)
        self.time_label.set_style_text_font(lv.font_number72, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.time_label.set_text('--:--:--')

        self.bat_label = lv.label(self.scr)
        self.bat_label.align(lv.ALIGN.BOTTOM_MID, 0, -10)
        self.bat_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.bat_label.set_text('BBB%')

        self.step_label = lv.label(self.scr)
        self.step_label.align(lv.ALIGN.LEFT_MID, 50, 60)
        self.step_label.set_style_text_font(lv.font_extra_symbols, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.step_label.set_text(fonts.SYMBOL.WALK + ' -- -- KM')

        self.ble_label = lv.label(self.scr)
        self.ble_label.align(lv.ALIGN.CENTER, 85, -60)
        self.ble_label.set_text(lv.SYMBOL.BLUETOOTH)
        if not hal.ble.connected():
            self.ble_label.set_style_text_color(lv.color_hex(0xBBBBBB), lv.PART.MAIN | lv.STATE.DEFAULT)

        self.update_display_task.start()

    def on_covered(self):
        self.update_display_task.stop()

    def on_cover_exit(self):
        self.update_display_task.start()
        self.refresh_event_cb(0)

    def update_display(self):
        lt = time.localtime()
        self.date_label.set_text('{:0>4d}-{:0>2d}-{:0>2d} {}'.format(*lt[:3], _WEEKDAY_NAMES[lt[6]]))
        self.time_label.set_text('{:0>2d}:{:0>2d}:{:0>2d}'.format(*lt[3:6]))
        bat_stat = hal.battery.dump()
        if bat_stat[3]:
            self.bat_label.set_text(lv.SYMBOL.CHARGE)
        else:
            self.bat_label.set_text('{:>3d}%'.format(bat_stat[2]))
        steps = hal.imu.get_step()
        length = (settingsdb.get('step_length', 50) * steps) / 100000
        self.step_label.set_text(fonts.SYMBOL.WALK + ' {:d}  {:.2f} KM'.format(steps, length))

    def refresh_event_cb(self, event):
        if hal.ble.connected():
            self.ble_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        else:
            self.ble_label.set_style_text_color(lv.color_hex(0xBBBBBB), lv.PART.MAIN | lv.STATE.DEFAULT)

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.TOP:
            QuickSettings().launch(lv.SCR_LOAD_ANIM.OVER_TOP)
        if gesture == lv.DIR.BOTTOM:
            NotificationCenter().launch(lv.SCR_LOAD_ANIM.OVER_BOTTOM)
        if gesture == lv.DIR.LEFT:
            Launcher().launch(lv.SCR_LOAD_ANIM.OVER_LEFT)
        if gesture == lv.DIR.RIGHT:
            launch_app('apps.calendar_app', lv.SCR_LOAD_ANIM.OVER_RIGHT)
