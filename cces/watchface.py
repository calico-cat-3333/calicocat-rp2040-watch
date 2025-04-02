import lvgl as lv
import time
import gc

from .activity import Activity, REFRESHON
from .activity import AskYesNoActivity
from .task_scheduler import Task
from . import gadgetbridge
from . import hal
from . import settingsdb
from .appmgr import Launcher

from .notification import NotificationCenter

class WatchFaceAtivity(Activity):
    def __init__(self):
        self.update_display_task = Task(self.update_display, 1000) # update display every 1 secs
        self.number_font = lv.binfont_create("S:fonts/number_72.bin")

    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.refresh_on = REFRESHON.BLE_CONNECTION
        self.sidekey_exit = False
        self.date_label = lv.label(self.scr)
        self.date_label.align(lv.ALIGN.CENTER, 0, -60)
        self.date_label.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.date_label.set_text('YYYY-MM-DD')

        self.time_label = lv.label(self.scr)
        self.time_label.align(lv.ALIGN.CENTER, 0, 0)
        self.time_label.set_style_text_font(self.number_font, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.time_label.set_text('--:--:--')

        self.bat_label = lv.label(self.scr)
        self.bat_label.align(lv.ALIGN.BOTTOM_MID, 0, -10)
        self.bat_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.bat_label.set_text('BBB%')

        self.step_label = lv.label(self.scr)
        self.step_label.align(lv.ALIGN.CENTER, -50, 60)
        self.step_label.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.step_label.set_text('steps:--')

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

    def update_display(self):
        lt = time.localtime()
        self.date_label.set_text('{:0>4d}-{:0>2d}-{:0>2d}'.format(*lt[:3]))
        self.time_label.set_text('{:0>2d}:{:0>2d}:{:0>2d}'.format(*lt[3:6]))
        bat_stat = hal.battery.dump()
        if bat_stat[3]:
            self.bat_label.set_text(lv.SYMBOL.CHARGE + str(bat_stat[1]))
        else:
            self.bat_label.set_text('{:>3d}%'.format(bat_stat[2]) + str(bat_stat[1]))
        self.step_label.set_text('steps:{:d}'.format(hal.imu.get_step()))

    def yesclick(self):
        settingsdb.put('do_not_disturb', True)
        gadgetbridge.send_msg('info', 'DND Enable!')

    def noclickcb(self):
        settingsdb.put('do_not_disturb', False)
        gadgetbridge.send_msg('info', 'DND Disable!')
        hal.buzzer.beep()

    def refresh_event_cb(self, event):
        if hal.ble.connected():
            self.ble_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        else:
            self.ble_label.set_style_text_color(lv.color_hex(0xBBBBBB), lv.PART.MAIN | lv.STATE.DEFAULT)

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.TOP:
            state = '勿扰已启用\n' if settingsdb.get('do_not_disturb', False) else '勿扰已禁用\n'
            AskYesNoActivity(title = 'DND',
                             text = state + '启用请勿打扰?',
                             on_yes_clicked = self.yesclick,
                             on_no_clicked = self.noclickcb,
                             yes_label_text = 'ON',
                             no_label_text = 'OFF',
                             exit_anim = lv.SCR_LOAD_ANIM.OVER_BOTTOM
                             ).launch(lv.SCR_LOAD_ANIM.OVER_TOP)
        if gesture == lv.DIR.BOTTOM:
            NotificationCenter().launch(lv.SCR_LOAD_ANIM.OVER_BOTTOM)
        if gesture == lv.DIR.LEFT:
            Launcher().launch(lv.SCR_LOAD_ANIM.OVER_LEFT)
