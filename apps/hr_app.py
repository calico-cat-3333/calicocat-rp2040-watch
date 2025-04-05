import lvgl as lv

from cces.appmgr import AppMeta
from cces.activity import Activity, fonts
from cces import hal, powermanager
from cces.task_scheduler import Task
from micropython import const

_CHART_POINT_COUNT = const(10)

class MainActivity(Activity):
    def __init__(self):
        self.update_task = Task(self.update_display, 2000)

    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.BPM = lv.label(self.scr)
        self.BPM.set_text('BPM')
        self.BPM.align(lv.ALIGN.CENTER, 40, -80)

        self.heartrate = lv.label(self.scr)
        self.heartrate.align(lv.ALIGN.RIGHT_MID, -105, -60)
        self.heartrate.set_style_text_align(lv.TEXT_ALIGN.RIGHT, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.heartrate.set_style_text_font(lv.font_number72, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.heartrate.set_text('---')

        self.spo2 = lv.label(self.scr)
        self.spo2.set_style_text_align(lv.TEXT_ALIGN.RIGHT, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.spo2.align(lv.ALIGN.CENTER, 70, -40)
        self.spo2.set_text("SpO2\n---%")

        self.hr_history_range_high = 140

        self.hr_history = lv.chart(self.scr)
        self.hr_history.set_size(155, 100)
        self.hr_history.align(lv.ALIGN.BOTTOM_MID, 10, -30)
        self.hr_history.set_type(lv.chart.TYPE.BAR)
        self.hr_history.set_point_count(_CHART_POINT_COUNT)
        self.hr_history.set_range(lv.chart.AXIS.PRIMARY_Y, 60, self.hr_history_range_high)

        self.hr_history_Yaxis1 = lv.scale(self.scr)
        self.hr_history_Yaxis1.set_mode(lv.scale.MODE.VERTICAL_LEFT)
        self.hr_history_Yaxis1.set_size(50, 100)
        self.hr_history_Yaxis1.align_to(self.hr_history, lv.ALIGN.OUT_LEFT_MID, 0, 0)
        self.hr_history_Yaxis1.set_style_pad_ver(self.hr_history.get_first_point_center_offset(), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.hr_history_Yaxis1.set_range(50, self.hr_history_range_high)
        self.hr_history_Yaxis1.set_total_tick_count(5)
        self.hr_history_Yaxis1.set_major_tick_every(1)

        self.hr_history_hrdata = self.hr_history.add_series(lv.color_hex(0xFF0000), lv.chart.AXIS.PRIMARY_Y)
        #self.hr_history.set_all_values(self.hr_history_hrdata, 0)
        self.hr_list = [0] * _CHART_POINT_COUNT
        self.hr_history.set_ext_y_array(self.hr_history_hrdata, self.hr_list)

        hal.hartrate.start_measure()
        powermanager.prevent_sleep(True)
        self.update_task.start()

    def update_display(self):
        hr = hal.hartrate.calculate_hr()
        spo2 = hal.hartrate.calculate_spo2()
        if hr != -1:
            self.heartrate.set_text('{: >3d}'.format(hr))
            #self.hr_history.set_next_value(self.hr_history_hrdata, hr)
            if 0 not in self.hr_list:
                self.hr_list.pop(0)
                self.hr_list.append(hr)
            else:
                self.hr_list[self.hr_list.index(0)] = hr
            self.hr_history.set_ext_y_array(self.hr_history_hrdata, self.hr_list)
            vmax = max(self.hr_list)
            if vmax > self.hr_history_range_high or (vmax > 50 and vmax < self.hr_history_range_high - 10):
                self.hr_history_range_high = ((max(self.hr_list) // 10) + 1) * 10
                self.hr_history.set_range(lv.chart.AXIS.PRIMARY_Y, 50, self.hr_history_range_high)
                self.hr_history_Yaxis1.set_range(50, self.hr_history_range_high)
        if spo2 != -1:
            self.spo2.set_text('SpO2\n{: >3d}%'.format(spo2))

    def before_exit(self):
        self.update_task.stop()
        powermanager.prevent_sleep(False)
        hal.hartrate.stop_measure()

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.RIGHT:
            self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

appmeta = AppMeta('心率', fonts.SYMBOL.HEART_RATE, MainActivity)