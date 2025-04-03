import lvgl as lv
import sys
import os
import machine

from cces.appmgr import AppMeta
from cces.activity import Activity, InfoActivity, AskYesNoActivity, NumberInputActivity, SliderActivity, fonts
from cces import hal
from cces import notification
from cces.log import log
from cces import settingsdb

class MainActivity(Activity):
    def __init__(self):
        # 设置项目名称，图标，类型（i(nput number), s(witch), None） callback, 附加参数
        # 除 None 类型外，附加参数第一个一定是设置项目键，第二个是默认值，剩余内容可自定义, 此项会在 callback 中作为第二个参数，此项的目的是复用代码
        self.objlist = [('请勿打扰', fonts.SYMBOL.BELL_DISABLE, 's', self.set_bool_obj, ('do_not_disturb', False, None)),
                        ('亮度(%)', fonts.SYMBOL.SUN, 'i', self.set_slider_obj, ('display_brightness', 100, hal.dispdev.set_brightness, 'Brightness', '%', 1, 100, None, hal.dispdev.set_brightness, 5)),
                        ('熄屏(s)', lv.SYMBOL.IMAGE, 'i', self.set_slider_obj, ('screenoff_timeout', 100, None, 'ScreenOff', 's', 10, 120, None, None, 10)),
                        ('音量(%)', lv.SYMBOL.VOLUME_MAX, 'i', self.set_slider_obj, ('sound_volume', 100, hal.buzzer.set_volume, 'Volume', '%', 0, 100, lambda _: hal.buzzer.beep(), hal.buzzer.set_volume, 5)),
                        '关于我',
                        ('身高(cm)', fonts.SYMBOL.USER_CONFIG, 'i', self.set_input_number_obj, ('user_height', 0, None, '身高(cm):', 1, 300)),
                        ('体重(kg)', fonts.SYMBOL.WEIGHT, 'i', self.set_input_number_obj, ('user_weight', 0, None, '体重(kg):', 1, 300)),
                        ('步长(cm)', fonts.SYMBOL.SHOE_PRINT, 'i', self.set_input_number_obj, ('user_step_length', 50, None, '步长(cm):', 1, 200)),
                        '高级',
                        ('关于', fonts.SYMBOL.CHIP, None, self.about_info, None),
                        ('重启', lv.SYMBOL.POWER, None, self.machine_reset, None),
                        ('重置', lv.SYMBOL.REFRESH, None, self.machine_restore, None),
                        ]

    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.settings_list = lv.list(self.scr)
        self.settings_list.set_size(200, 240)
        self.settings_list.align(lv.ALIGN.CENTER, 20, 0)
        self.settings_list.set_style_border_side(lv.BORDER_SIDE.NONE, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.settings_list.set_style_text_font(lv.font_extra_symbols, lv.PART.MAIN | lv.STATE.DEFAULT)
        title = self.settings_list.add_text(lv.SYMBOL.SETTINGS + ' 设置',)
        title.set_style_pad_bottom(10, lv.PART.MAIN | lv.STATE.DEFAULT)
        title.set_style_pad_top(20, lv.PART.MAIN | lv.STATE.DEFAULT)

        for obj in self.objlist:
            if isinstance(obj, str):
                text = self.settings_list.add_text(obj)
                text.set_style_pad_ver(10, lv.PART.MAIN | lv.STATE.DEFAULT)
                continue
            btn = self.settings_list.add_button(obj[1], obj[0])
            btn.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.SPACE_EVENLY)
            #btn.set_style_pad_ver(15, lv.PART.MAIN | lv.STATE.DEFAULT)
            btn.set_height(50)
            img = btn.get_child(0)
            img.set_width(20)
            img.set_inner_align(lv.image.ALIGN.CENTER)

            if obj[2] == 's':
                switch = lv.switch(btn)
                switch.align(lv.ALIGN.RIGHT_MID, 0, 0)
                switch.set_size(45, 25)
                if settingsdb.get(obj[4][0], obj[4][1]):
                    switch.add_state(lv.STATE.CHECKED)
                switch.add_event_cb(lambda event, obj=obj: obj[3](event, obj[4]), lv.EVENT.VALUE_CHANGED, None)
                continue
            else:
                current_label = lv.label(btn)
                current_label.align(lv.ALIGN.RIGHT_MID, 0, 0)
                if obj[2] == 'i':
                    current_label.set_text(str(settingsdb.get(obj[4][0], obj[4][1])))
                    current_label.set_width(40)
                else:
                    current_label.set_text(lv.SYMBOL.RIGHT)
                current_label.set_style_text_align(lv.TEXT_ALIGN.RIGHT, lv.PART.MAIN | lv.STATE.DEFAULT)
                btn.add_event_cb(lambda event, obj=obj: obj[3](event, obj[4]), lv.EVENT.CLICKED, None)

        self.exit_btn = lv.button(self.scr)
        self.exit_btn.align(lv.ALIGN.LEFT_MID, 0, 0)
        self.exit_btn.set_size(40, 240)
        self.exit_btn.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.exit_btn.add_event_cb(self.exit_btn_cb, lv.EVENT.CLICKED, None)
        self.exit_btn_label = lv.label(self.exit_btn)
        self.exit_btn_label.set_text(lv.SYMBOL.LEFT)
        self.exit_btn_label.align(lv.ALIGN.RIGHT_MID, 0, 0)
        self.exit_btn_label.set_style_text_font(lv.font_montserrat_24, 0)

    def before_exit(self):
        settingsdb.save_settings()

    def exit_btn_cb(self, event):
        self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.RIGHT:
            self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

    def set_bool_obj(self, event, attr):
        # attr[2] 是一个 callback 接受一个 bool 作为参数，数字是 switch 的现在状态，该项可以为 None
        target = event.get_target_obj()
        state = target.has_state(lv.STATE.CHECKED)
        settingsdb.put(attr[0], state)
        if attr[2] != None:
            attr[2](state)

    def set_slider_obj(self, event, attr):
        # attr[2] 是一个 callback 接受一个数字作为参数，数字是 slider 的当前值，该项可以为 None
        # attr[3] 是 SliderActivity 的 标题
        # attr[4] 是 SliderActivity 的 单位
        # attr[5-6] 是 SliderActivity 的最小值和最大值
        # attr[7] 是 SliderActivity 的 on_slider_release callback，该项可以为 None
        # attr[8] 是 SliderActivity 的 on_value_change callback，该项可以为 None
        # attr[9] 是步进值
        current_label = event.get_target_obj().get_child(2)
        def set_value(value):
            settingsdb.put(attr[0], value)
            current_label.set_text(str(value))
            if attr[2] != None:
                attr[2](value)
        SliderActivity(title = attr[3],
                       number_min = attr[5],
                       number_max = attr[6],
                       number_default = settingsdb.get(attr[0], attr[1]),
                       unit = attr[4],
                       on_yes_clicked = set_value,
                       on_no_clicked = set_value,
                       on_slider_release = attr[7],
                       on_value_change = attr[8],
                       step = attr[9],
                       exit_anim = lv.SCR_LOAD_ANIM.OVER_RIGHT
                       ).launch(lv.SCR_LOAD_ANIM.OVER_LEFT)

    def set_input_number_obj(self, event, attr):
        # attr[2] 是一个 callback 接受一个数字作为参数，数字是输入的值，该项可以为 None
        # attr[3] 是 NumberInputActivity 的 提示
        # attr[4-5] 是 NumberInputActivity 的最小值和最大值
        current_label = event.get_target_obj().get_child(2)
        def set_value(value):
            settingsdb.put(attr[0], value)
            current_label.set_text(str(value))
            if attr[2] != None:
                attr[2](value)
        NumberInputActivity(title = attr[3],
                            number_min = attr[4],
                            number_max = attr[5],
                            on_ok_clicked = set_value,
                            exit_anim = lv.SCR_LOAD_ANIM.OVER_RIGHT
                            ).launch(lv.SCR_LOAD_ANIM.OVER_LEFT)

    def machine_reset(self, event, attr):
        def do_reset():
            try:
                machine.reset()
            except:
                machine.soft_reset()
        AskYesNoActivity(title = 'Reset',
                         text = '重启设备',
                         on_yes_clicked = do_reset,
                         exit_anim = lv.SCR_LOAD_ANIM.OVER_RIGHT
                         ).launch(lv.SCR_LOAD_ANIM.OVER_LEFT)

    def machine_restore(self, event, attr):
        def do_restore():
            settingsdb._settings.clear()
            settingsdb.save_settings()
            try:
                machine.reset()
            except:
                machine.soft_reset()
        AskYesNoActivity(title = 'Restore',
                         text = '恢复出厂设置',
                         on_yes_clicked = do_restore,
                         exit_anim = lv.SCR_LOAD_ANIM.OVER_RIGHT
                         ).launch(lv.SCR_LOAD_ANIM.OVER_LEFT)

    def about_info(self, event, attr):
        try:
            osinfo = os.uname().release
        except:
            osinfo = '未知'
        info_text = 'CCES 智能手表系统\nCalicocat 制作\nmicropython 版本：' + osinfo + '\n平台：' + sys.platform
        InfoActivity(title = 'ABOUT',
                     text = info_text,
                     exit_anim = lv.SCR_LOAD_ANIM.OVER_RIGHT
                     ).launch(lv.SCR_LOAD_ANIM.OVER_LEFT)

appmeta = AppMeta('设置', lv.SYMBOL.SETTINGS, MainActivity)