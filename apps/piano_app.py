import lvgl as lv

from cces.appmgr import AppMeta
from cces.activity import Activity, fonts
from cces import hal

class MainActivity(Activity):
    def __init__(self):
        self.btn_map = ['\n1', '\n2', '\n3', '\n4', '\n', '\n5', '\n6', '\n7', '.\n1', '']
        self.tones = (262, 294, 330, 349, 392, 440, 494, 523)  # C大调音阶

    def setup(self):
        self.keys = lv.buttonmatrix(self.scr)
        self.keys.align(lv.ALIGN.CENTER, 0, 0)
        self.keys.set_map(self.btn_map)
        self.keys.set_size(200, 150)
        self.keys.add_event_cb(self.bm_click_cb, lv.EVENT.VALUE_CHANGED, None)
        self.keys.set_style_border_side(lv.BORDER_SIDE.NONE, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.keys.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN | lv.STATE.DEFAULT)

        self.exit_btn = lv.button(self.scr)
        self.exit_btn.align(lv.ALIGN.BOTTOM_MID, 0, -10)
        self.exit_btn.add_event_cb(self.exit_btn_cb, lv.EVENT.CLICKED, None)
        self.exit_btn_label = lv.label(self.exit_btn)
        self.exit_btn_label.align(lv.ALIGN.CENTER, 0, 0)
        self.exit_btn_label.set_text('EXIT')

        self.title_label = lv.label(self.scr)
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 10)
        self.title_label.set_text('蜂鸣器琴')

    def bm_click_cb(self, _):
        n = self.keys.get_selected_button()
        hal.buzzer.beep(self.tones[n])

    def exit_btn_cb(self, _):
        self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.RIGHT:
            self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

appmeta = AppMeta('蜂鸣器琴', lv.SYMBOL.AUDIO, MainActivity)