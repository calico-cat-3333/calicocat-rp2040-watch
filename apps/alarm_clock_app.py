import lvgl as lv
import sys
import gc

from cces.appmgr import AppMeta
from cces.activity import Activity, InfoActivity
from cces import hal, settingsdb
from cces.daily_scheduler import DailyTask, list_by_tag
from cces.task_scheduler import Task
from cces.log import log

alarms_pair_list = []

def load_alarms():
    alarms_list = settingsdb.get('alarm_clocks', [])
    for alarm in alarms_list:
        dt = DailyTask(alarm_clock_alarm, (alarm['h'], alarm['m']), tag='alarm_clock', weekdays=alarm['rep'], enabled=bool(alarm.get('on', 1)))
        alarms_pair_list.append((alarm, dt))

def alarm_clock_alarm():
    beep_repeat_task.start()
    InfoActivity('Alarm', '时间到！', beep_repeat_task.stop).launch()

def on_system_start():
    global beep_repeat_task
    beep_repeat_task = Task(hal.buzzer.play, 1000)
    beep_repeat_task.set_args([4000,0,4000])

    load_alarms()

class SetAlarm(Activity):
    def __init__(self, alarm_pair):
        self.alarm_pair = alarm_pair
        self.btn_map = ['周一', '周二', '周三', '周四', '\n', ' ', '周五', '周六', '周日', ' ', '']
        self.ctrl_map = [2 | lv.buttonmatrix.CTRL.CHECKABLE] * 4 + [ 1 | lv.buttonmatrix.CTRL.HIDDEN] + [2 | lv.buttonmatrix.CTRL.CHECKABLE] * 3 + [ 1 | lv.buttonmatrix.CTRL.HIDDEN]

    def setup(self):
        self.colon = lv.label(self.scr)
        self.colon.set_text(":")
        self.colon.align(lv.ALIGN.TOP_MID, 0, 50)
        self.colon.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.hour = lv.dropdown(self.scr)
        self.hour.set_options("00\n01\n02\n03\n04\n05\n06\n07\n08\n09\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23")
        self.hour.set_width(60)
        self.hour.align(lv.ALIGN.TOP_MID, -40, 45)
        self.hour.set_selected(self.alarm_pair[0]['h'], False)

        self.minute = lv.dropdown(self.scr)
        self.minute.set_options("00\n01\n02\n03\n04\n05\n06\n07\n08\n09\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n25\n26\n27\n28\n29\n30\n31\n32\n33\n34\n35\n36\n37\n38\n39\n40\n41\n42\n43\n44\n45\n46\n47\n48\n49\n50\n51\n52\n53\n54\n55\n56\n57\n58\n59")
        self.minute.set_width(60)
        self.minute.align(lv.ALIGN.TOP_MID, 40, 45)
        self.minute.set_selected(self.alarm_pair[0]['m'], False)

        self.title = lv.label(self.scr)
        self.title.set_text("设置闹钟")
        self.title.align(lv.ALIGN.TOP_MID, 0, 10)

        self.dayselect = lv.buttonmatrix(self.scr)
        self.dayselect.align(lv.ALIGN.CENTER, 0, 15)
        self.dayselect.set_map(self.btn_map)
        self.dayselect.set_ctrl_map(self.ctrl_map)
        self.dayselect.set_size(200, 100)
        self.dayselect.add_event_cb(self.dayselect_cb, lv.EVENT.VALUE_CHANGED, None)
        w = self.alarm_pair[0]['rep']
        for i in range(0, 7):
            if w & (1 << i):
                c = i if i < 4 else i + 1
                self.dayselect.set_button_ctrl(c, lv.buttonmatrix.CTRL.CHECKED)

        self.done = lv.button(self.scr)
        self.done.set_size(119, 50)
        self.done.align(lv.ALIGN.BOTTOM_LEFT, 0, 0)
        self.done.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.done.add_event_cb(self.done_cb, lv.EVENT.CLICKED, None)

        self.done_label = lv.label(self.done)
        self.done_label.set_text(lv.SYMBOL.OK)
        self.done_label.align(lv.ALIGN.RIGHT_MID, -15, 0)

        self.remove = lv.button(self.scr)
        self.remove.set_size(119, 50)
        self.remove.align(lv.ALIGN.BOTTOM_RIGHT, 0, 0)
        self.remove.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.remove.set_style_bg_color(lv.color_hex(0xFF0000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.remove.add_event_cb(self.remove_cb, lv.EVENT.CLICKED, None)

        self.remove_label = lv.label(self.remove)
        self.remove_label.set_text(lv.SYMBOL.TRASH)
        self.remove_label.align(lv.ALIGN.LEFT_MID, 15, 0)

    def dayselect_cb(self, event):
        w = self.alarm_pair[0]['rep']
        n = self.dayselect.get_selected_button()
        p = n if n < 4 else n - 1
        print(p)
        if not self.dayselect.has_button_ctrl(n, lv.buttonmatrix.CTRL.CHECKED):
            w = w | (1 << p)
        else:
            w = w & (~(1 << p))
        self.alarm_pair[0]['rep'] = w


    def done_cb(self, evnet):
        h = self.hour.get_selected()
        m = self.minute.get_selected()
        self.alarm_pair[0]['h'] = h
        self.alarm_pair[0]['m'] = m
        if self.alarm_pair[0]['rep'] == 0:
            self.alarm_pair[0]['on'] = 0
        else:
            self.alarm_pair[0]['on'] = 1

        self.alarm_pair[1].set_starttime((h, m), self.alarm_pair[0]['rep'])
        self.alarm_pair[1].start()
        self.exit()

    def remove_cb(self, event):
        alarms_pair_list.remove(self.alarm_pair)
        self.alarm_pair[1].remove()
        settingsdb.get('alarm_clocks', []).remove(self.alarm_pair[0])
        self.exit()

class MainActivity(Activity):
    def __init__(self):
        self.weekday_name = ['一', '二', '三', '四', '五', '六', '日']

    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.set_alarm_list = lv.list(self.scr)
        self.set_alarm_list.set_size(200, 220)
        self.set_alarm_list.align(lv.ALIGN.CENTER, 20, 0)
        self.set_alarm_list.set_style_border_side(lv.BORDER_SIDE.NONE, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.exit_btn = lv.button(self.scr)
        self.exit_btn.align(lv.ALIGN.LEFT_MID, 0, 0)
        self.exit_btn.set_size(40, 240)
        self.exit_btn.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.exit_btn.add_event_cb(self.exit_btn_cb, lv.EVENT.CLICKED, None)
        self.exit_btn_label = lv.label(self.exit_btn)
        self.exit_btn_label.set_text(lv.SYMBOL.LEFT)
        self.exit_btn_label.align(lv.ALIGN.RIGHT_MID, 0, 0)
        self.exit_btn_label.set_style_text_font(lv.font_montserrat_24, 0)

        self.update_display()

    def update_display(self):
        title = self.set_alarm_list.add_text('闹钟')
        title.set_style_pad_ver(10, lv.PART.MAIN | lv.STATE.DEFAULT)

        for alarm_pair in alarms_pair_list:
            btn = self.set_alarm_list.add_button(None, '{:0>2d}:{:0>2d}\n'.format(alarm_pair[0]['h'], alarm_pair[0]['m']) + self.get_weekdays_str(alarm_pair[0]['rep']))
            btn.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.SPACE_EVENLY)
            btn.add_event_cb(lambda e, ap=alarm_pair: self.set_alarm(ap), lv.EVENT.CLICKED, None)
            btn.set_style_pad_ver(15, lv.PART.MAIN | lv.STATE.DEFAULT)

            switch = lv.switch(btn)
            switch.align(lv.ALIGN.RIGHT_MID, 0, 0)
            switch.set_size(45, 25)
            if alarm_pair[1].enabled:
                switch.add_state(lv.STATE.CHECKED)
            switch.add_event_cb(lambda e, ap=alarm_pair: self.alarm_toggle(e, ap), lv.EVENT.VALUE_CHANGED, None)

        nbtn = self.set_alarm_list.add_button(None, lv.SYMBOL.PLUS + ' 新建...')
        nbtn.add_event_cb(self.new_alarm, lv.EVENT.CLICKED, None)
        nbtn.set_style_pad_ver(15, lv.PART.MAIN | lv.STATE.DEFAULT)

    def get_weekdays_str(self, weekdays):
        if weekdays == 0:
            return '不重复'
        if weekdays == 0b1111111:
            return '每天'
        if weekdays == 0b0011111:
            return '周一到周五'
        if weekdays == 0b1100000:
            return '周末'
        s = ''
        for i in range(0, 7):
            if weekdays & (1 << i):
                s = s + self.weekday_name[i]
        return s

    def set_alarm(self, alarm_pair):
        SetAlarm(alarm_pair).launch()

    def new_alarm(self, *args):
        na = {'h': 8, 'm': 0, 'rep': 0, 'on': 0}
        ndt = DailyTask(alarm_clock_alarm, (8, 0), tag='alarm_clock', weekdays=0, enabled=False)
        nap = (na, ndt)
        settingsdb.get('alarm_clocks', []).append(na)
        alarms_pair_list.append(nap)
        SetAlarm(nap).launch()

    def alarm_toggle(self, event, alarm_pair):
        target = event.get_target_obj()
        state = target.has_state(lv.STATE.CHECKED)
        if state:
            alarm_pair[0]['on'] = 1
            alarm_pair[1].start()
        else:
            alarm_pair[0]['on'] = 0
            alarm_pair[1].stop()

    def on_cover_exit(self):
        self.update_display()

    def on_covered(self):
        self.set_alarm_list.clean()
        gc.collect()

    def before_exit(self):
        settingsdb.save_settings()

    def exit_btn_cb(self, event):
        self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.RIGHT:
             self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

appmeta = AppMeta('闹钟', lv.SYMBOL.BELL, MainActivity, on_system_start)