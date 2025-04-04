import lvgl as lv

from cces.appmgr import AppMeta
from cces.activity import Activity
from cces import hal

muyu_img = lv.image_dsc_t({
    'header': {
        'cf': lv.COLOR_FORMAT.A1,
        'w': 20,
        'h': 20,
    },
    'data_size': 60,
    'data': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\x80\x03\xff\xc0\x07\xff\xc0\x0f\xff\xe0\x0f\xff\xe0\x0f\xdf\xe0\x1f\x80\x00\x7f\xdf\xe0\xff\xff\xe0\xff\xff\xe0\x7f\xff\xc0\x1f\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
})

class MainActivity(Activity):
    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.knock_btn = lv.button(self.scr)
        self.knock_btn.set_size(100, 100)
        self.knock_btn.align(lv.ALIGN.CENTER, 0, 0)
        self.knock_btn.add_event_cb(self.knock_btn_cb, lv.EVENT.CLICKED, None)
        self.knock_btn.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.muyu_img = lv.image(self.knock_btn)
        self.muyu_img.align(lv.ALIGN.CENTER, 0, 0)
        self.muyu_img.set_src(muyu_img)
        self.muyu_img.set_antialias(False)
        self.muyu_img.set_scale(1024)

        self.gongde_label = lv.label(self.scr)
        self.gongde_label.align(lv.ALIGN.TOP_MID, 0, 25)
        self.gongde_label.set_text('电子木鱼\n功德 + 0')
        self.gongde_label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.gd_num = 0

        self.exit_btn = lv.button(self.scr)
        self.exit_btn.align(lv.ALIGN.BOTTOM_MID, 0, -20)
        self.exit_btn.add_event_cb(self.exit_btn_cb, lv.EVENT.CLICKED, None)
        self.exit_btn_label = lv.label(self.exit_btn)
        self.exit_btn_label.align(lv.ALIGN.CENTER, 0, 0)
        self.exit_btn_label.set_text('EXIT')

    def knock_btn_cb(self, _):
        self.gd_num = self.gd_num + 1
        self.gongde_label.set_text('电子木鱼\n功德 + ' + str(self.gd_num))
        hal.buzzer.beep()

    def exit_btn_cb(self, _):
        self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.RIGHT:
            self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

appmeta = AppMeta('电子木鱼', muyu_img, MainActivity)