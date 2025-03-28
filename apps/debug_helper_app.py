import lvgl as lv
import sys

from cces.appmgr import AppMeta
from cces.activity import Activity, InfoActivity, AskYesNoActivity, NumberInputActivity, SliderActivity
from cces import hal
from cces import notification
from cces.log import log

class MainActivity(Activity):
    def __init__(self):
        self.fl = []
        self.fl.append(('notify send', self.send_notify))
        self.nid = None

        self.fl.append(('notify remove', self.remove_notify))
        self.fl.append(('info', self.info_example))
        self.fl.append(('askyesno', self.askyesno_example))
        self.fl.append(('input number', self.input_number_example))
        self.fl.append(('slider', self.slider_example))

    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.dlst = lv.list(self.scr)
        self.dlst.set_size(200, 220)
        self.dlst.align(lv.ALIGN.CENTER, 20, 0)

        for f in self.fl:
            btn = self.dlst.add_button(lv.SYMBOL.FILE, f[0])
            btn.add_event_cb(f[1], lv.EVENT.CLICKED, None)
            btn.set_style_pad_ver(15, lv.PART.MAIN | lv.STATE.DEFAULT)
            img = btn.get_child(0)
            img.set_width(20)
            img.set_inner_align(lv.image.ALIGN.CENTER)

        self.exit_btn = lv.button(self.scr)
        self.exit_btn.align(lv.ALIGN.LEFT_MID, 0, 0)
        self.exit_btn.set_size(40, 240)
        self.exit_btn.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.exit_btn.add_event_cb(self.exit_btn_cb, lv.EVENT.CLICKED, None)
        self.exit_btn_label = lv.label(self.exit_btn)
        self.exit_btn_label.set_text(lv.SYMBOL.LEFT)
        self.exit_btn_label.align(lv.ALIGN.RIGHT_MID, 0, 0)
        self.exit_btn_label.set_style_text_font(lv.font_montserrat_24, 0)

    def exit_btn_cb(self, event):
        self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.RIGHT:
             self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

    def send_notify(self, _):
        self.nid = notification.send('example notify', 'example notify text.')

    def remove_notify(self, _):
        if not self.nid:
            InfoActivity('Error', 'You Need Send notify before remove it').launch()
        notification.remove(self.nid)

    def info_example(self, _):
        def ok_click():
            log('ok clicked!')
        InfoActivity('title', 'text', ok_click).launch()

    def askyesno_example(self, _):
        def yes_click():
            log('yes clicked!')
        def no_click():
            log('no clicked!')
        AskYesNoActivity('title', 'text', yes_click, no_click).launch()

    def input_number_example(self, _):
        def getnumb(numb):
            log(numb)
        NumberInputActivity('title', -10, 10, getnumb).launch()

    def slider_example(self, _):
        def ok_cb(numb):
            log('ok', numb)
        def vc_cb(n):
            log('value change', n)
        def sr_cb(n):
            log('slider released', n)
        def no_cb(n):
            log('no', n)
        SliderActivity('title', 0, 100, 0, '%', ok_cb, no_cb, sr_cb, vc_cb).launch()

appmeta = AppMeta('测试器', lv.SYMBOL.FILE, MainActivity)