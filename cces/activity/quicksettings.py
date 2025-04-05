import lvgl as lv
import random

from .activity import Activity, REFRESHON
from . import fonts, styles
from .. import hal, settingsdb, gadgetbridge, notification

# 快速设置面板，用于表盘页上划

class QuickSettings(Activity):
    def __init__(self):
        self.btn_map = [fonts.SYMBOL.BELL_DISABLE + ' 请勿打扰', fonts.SYMBOL.COMMENT + ' 清空通知', '\n', fonts.SYMBOL.PHONE + ' 查找手机', fonts.SYMBOL.DICE[0] + ' 随机骰子', '']

    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.refresh_on = REFRESHON.BLE_CONNECTION
        self.bat_info = lv.label(self.scr)
        self.bat_info.align(lv.ALIGN.BOTTOM_MID, 0, -40)
        bs_text = ''
        bs = hal.battery.dump()
        if bs[3] == True:
            bs_text = bs_text + lv.SYMBOL.CHARGE + ' '
        if bs[2] < 20:
            bs_text = bs_text + lv.SYMBOL.BATTERY_EMPTY
        elif bs[2] < 40:
            bs_text = bs_text + lv.SYMBOL.BATTERY_1
        elif bs[2] < 60:
            bs_text = bs_text + lv.SYMBOL.BATTERY_2
        elif bs[2] < 80:
            bs_text = bs_text + lv.SYMBOL.BATTERY_3
        else:
            bs_text = bs_text + lv.SYMBOL.BATTERY_FULL
        bs_text = bs_text + ' {:0>2d}%, {:.2f}V'.format(bs[2], bs[0])
        self.bat_info.set_text(bs_text)

        self.settings_panel = lv.buttonmatrix(self.scr)
        self.settings_panel.set_size(200, 125)
        self.settings_panel.align(lv.ALIGN.CENTER, 0, -10)
        self.settings_panel.set_style_text_font(lv.font_extra_symbols, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.settings_panel.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.settings_panel.add_event_cb(self.settings_click, lv.EVENT.VALUE_CHANGED, None)
        self.settings_panel.set_style_border_side(lv.BORDER_SIDE.NONE, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.settings_panel.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.settings_panel.set_style_pad_hor(0, lv.PART.MAIN | lv.STATE.DEFAULT)

        if not settingsdb.get('do_not_disturb', False):
            self.btn_map[0] = lv.SYMBOL.BELL + ' 请勿打扰'

        self.settings_panel.set_map(self.btn_map)
        self.settings_panel.set_button_ctrl(0, lv.buttonmatrix.CTRL.CHECKABLE)
        self.settings_panel.set_button_ctrl(2, lv.buttonmatrix.CTRL.CHECKABLE)
        self.settings_panel.set_button_ctrl(1, lv.buttonmatrix.CTRL.CHECKED)
        self.settings_panel.set_button_ctrl(3, lv.buttonmatrix.CTRL.CHECKED)
        if settingsdb.get('do_not_disturb', False):
            self.settings_panel.set_button_ctrl(0, lv.buttonmatrix.CTRL.CHECKED)

        self.exit_btn = lv.button(self.scr)
        self.exit_btn.set_size(240, 45)
        self.exit_btn.align(lv.ALIGN.TOP_MID, 0, 0)
        self.exit_btn.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.exit_btn.add_style(styles.transparent_button, lv.PART.MAIN| lv.STATE.DEFAULT)
        self.exit_btn.set_style_border_side(lv.BORDER_SIDE.NONE, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.exit_btn.add_event_cb(self.exit_btn_cb, lv.EVENT.CLICKED, None)

        self.ble_status = lv.label(self.exit_btn)
        self.ble_status.align(lv.ALIGN.BOTTOM_MID, 0, 0)
        self.refresh_event_cb(0)

    def refresh_event_cb(self, event):
        if hal.ble.connected():
            self.ble_status.set_text(lv.SYMBOL.BLUETOOTH + ' 已连接')
        else:
            self.ble_status.set_text(lv.SYMBOL.BLUETOOTH + ' 未连接')

    def settings_click(self, event):
        b = self.settings_panel.get_selected_button()
        if b == 0:
            if settingsdb.get('do_not_disturb', False):
                settingsdb.put('do_not_disturb', False)
                gadgetbridge.send_msg('info', 'DND Disable!')
                self.btn_map[0] = lv.SYMBOL.BELL + ' 请勿打扰'
            else:
                settingsdb.put('do_not_disturb', True)
                gadgetbridge.send_msg('info', 'DND Enable!')
                self.btn_map[0] = fonts.SYMBOL.BELL_DISABLE + ' 请勿打扰'
            self.settings_panel.set_map(self.btn_map)
        elif b == 1:
            notification.clear_all()
        elif b == 2:
            if self.settings_panel.has_button_ctrl(2, lv.buttonmatrix.CTRL.CHECKED):
                gadgetbridge.find_phone(False)
            else:
                gadgetbridge.find_phone(True)
        elif b == 3:
            t = random.randint(0, 5)
            self.btn_map[4] = fonts.SYMBOL.DICE[t] + ' 随机骰子'
            self.settings_panel.set_map(self.btn_map)

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.BOTTOM:
            self.exit(lv.SCR_LOAD_ANIM.OVER_BOTTOM)

    def exit_btn_cb(self, event):
        self.exit(lv.SCR_LOAD_ANIM.OVER_BOTTOM)
