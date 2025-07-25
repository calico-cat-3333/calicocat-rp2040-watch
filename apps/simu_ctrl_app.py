import lvgl as lv
import sys
from random import randint

from cces.appmgr import AppMeta, launch_app
from cces.activity import Activity, InfoActivity, AskYesNoActivity, NumberInputActivity, SliderActivity, fonts
from cces import hal, gadgetbridge
from cces import notification
from cces.log import log

class MainActivity(Activity):
    def __init__(self):
        if sys.platform == 'rp2':
            log('should not load this app on real machine')
            self.fl = [('No use on', self.exit_btn_cb),
                       ('real machine', self.exit_btn_cb)
                       ]
        else:
            self.fl = [('bat adc', self.set_dummy_bat_value),
                       ('set step', self.set_dummy_setp_value),
                       ('tog ble', self.dummyble_tog),
                       ('GB weather', self.send_dummy_weather),
                       ('GB notify', self.send_dummy_notify),
                       ('weather_app', lambda _: launch_app('apps.weather_app')),
                       ('GB Music', self.send_dummy_music),
                       ('GB actfetch', self.send_dummy_actfetch),
                       ]

    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.dlst = lv.list(self.scr)
        self.dlst.set_size(200, 240)
        self.dlst.align(lv.ALIGN.CENTER, 20, 0)
        self.dlst.set_style_border_side(lv.BORDER_SIDE.NONE, lv.PART.MAIN | lv.STATE.DEFAULT)
        title = self.dlst.add_text('SimuCtrl')
        title.set_style_pad_bottom(10, lv.PART.MAIN | lv.STATE.DEFAULT)
        title.set_style_pad_top(20, lv.PART.MAIN | lv.STATE.DEFAULT)

        for f in self.fl:
            btn = self.dlst.add_button(lv.SYMBOL.FILE, f[0])
            btn.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.SPACE_EVENLY)
            btn.add_event_cb(f[1], lv.EVENT.CLICKED, None)
            #btn.set_style_pad_ver(15, lv.PART.MAIN | lv.STATE.DEFAULT)
            btn.set_height(50)
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

    def gbinfo(self, _):
        gadgetbridge.send_msg('info', 'test info')

    def dummyble_tog(self, _):
        hal.ble.dummyconnect(not hal.ble.connected())

    def send_dummy_weather(self, _):
        codes = [800, 801, 803, 200, 300, 500, 600, 700, 511, 771, 781]
        strs = ['晴', '多云', '阴', '雷暴', '小雨', '大雨', '雪', '雾', '冻雨', '狂风', '龙卷风']
        ctmp = [0, 1, 2, 3, 4, 5, -10, 7, -5, 9, 15]
        tmpl = [-5, -4, -3, -2, 0, 3, -15, 4, -9, 3, 10]
        tmph = [5, 6, 7, 8, 9, 10, -1, 11, 0, 14, 20]
        r = randint(0, len(codes) - 1)
        rain = randint(0, 100)
        uv = randint(0, 15)
        wdir = randint(0, 359)
        wind = randint(0, 50) * 1.0
        hum = randint(0, 100)
        hal.ble.rx_line_buf.append('\x10GB({' + '"t":"weather","temp":{:d},"hi":{:d},"lo":{:d},"hum":{:d},"rain":{:d},"uv":{:d},"code":{:d},"txt":"{}","wind":{:f},"wdir":{:d},"loc":"\u957f\u6e05\u533a"'.format(ctmp[r] + 273, tmph[r] + 273, tmpl[r] + 273, hum, rain, uv, codes[r], strs[r], wind, wdir) + '})')

    def send_dummy_music(self, _):
        hal.ble.rx_line_buf.append('\x10GB({"t":"musicinfo","artist":"\u6d1b\u5929\u4f9d","album":"\u7acb\u6625","track":"\u7acb\u6625","dur":131,"c":-1,"n":1})')
        hal.ble.rx_line_buf.append('\x10GB({"t":"musicstate","state":"play","position":50,"shuffle":-1,"repeat":-1})')

    def set_dummy_bat_value(self, _):
        def setv(v):
            hal.battery.fake_adc_value = v
            log('set fake bat adc value:', v)
        NumberInputActivity('Dummy bat', 21845, 30000, setv, 25000).launch()

    def set_dummy_setp_value(self, _):
        def setv(v):
            hal.imu.dummy_step = v
            log('set fake step value:', v)
        NumberInputActivity('Dummy step', 0, 3000, setv).launch()

    def send_dummy_actfetch(self, _):
        hal.ble.rx_line_buf.append('\x10GB({"t":"actfetch","ts":0})')

    def send_dummy_notify(self, _):
        hal.ble.rx_line_buf.append('\x10GB({"t":"notify","id":1744169092,"src":"Gadgetbridge","title":"","subject":"Test","body":"Test","sender":"Test","tel":"Test"})')

appmeta = AppMeta('SimuCtrl', fonts.SYMBOL.TERMINAL, MainActivity)