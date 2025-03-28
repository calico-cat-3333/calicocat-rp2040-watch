import lvgl as lv

from . import Activity

class SliderActivity(Activity):
    def __init__(self, title, nmin=0, nmax=100, ndefault=0, unit='', on_yes_clicked=None, on_no_clicked=None, on_slider_release=None, on_value_change=None, yes_label_text='Yes', no_label_text='No', exit_anim=None):
        # on_yes_clicked, on_slider_release, on_value_change 需要接受一个参数，该参数为滑块的当前值
        # on_no_clicked 需要接受一个参数，该参数为传入的默认值
        self.title = title
        self.unit = unit
        self.number_min = nmin
        self.number_max = nmax
        self.number_default = ndefault
        self.on_yes_clicked = on_yes_clicked
        self.on_no_clicked = on_no_clicked
        self.on_slider_release = on_slider_release
        self.on_value_change = on_value_change
        self.yes_label_text = yes_label_text
        self.no_label_text = no_label_text
        self.exit_anim = exit_anim

    def setup(self):
        self.title_label = lv.label(self.scr)
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 30)
        self.title_label.set_width(160)
        self.title_label.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
        self.title_label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.title_label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.title_label.set_text(self.title)

        self.value_label = lv.label(self.scr)
        self.value_label.align(lv.ALIGN.CENTER, 0, -40)
        self.value_label.set_text(str(self.number_default) + self.unit)

        self.slider = lv.slider(self.scr)
        self.slider.set_size(150, 20)
        self.slider.align(lv.ALIGN.CENTER, 0, 0)
        self.slider.set_range(self.number_min, self.number_max)
        self.slider.set_value(self.number_default, False)
        self.slider.add_event_cb(self.slider_value_change_cb, lv.EVENT.VALUE_CHANGED, None)
        if self.on_slider_release != None:
            self.slider.add_event_cb(self.slider_release_cb, lv.EVENT.RELEASED, None)

        self.yes_btn = lv.button(self.scr)
        self.yes_btn.align(lv.ALIGN.BOTTOM_LEFT, 0, 0)
        self.yes_btn.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.yes_btn.set_size(119, 60)
        self.yes_btn.add_event_cb(self.yes_btn_click_cb, lv.EVENT.CLICKED, None)
        self.yes_btn_label = lv.label(self.yes_btn)
        self.yes_btn_label.align(lv.ALIGN.RIGHT_MID, 0, 0)
        self.yes_btn_label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.yes_btn_label.set_text(self.yes_label_text)

        self.no_btn = lv.button(self.scr)
        self.no_btn.align(lv.ALIGN.BOTTOM_RIGHT, 0, 0)
        self.no_btn.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.no_btn.set_size(119, 60)
        self.no_btn.add_event_cb(self.no_btn_click_cb, lv.EVENT.CLICKED, None)
        self.no_btn_label = lv.label(self.no_btn)
        self.no_btn_label.align(lv.ALIGN.LEFT_MID, 0, 0)
        self.no_btn_label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.no_btn_label.set_text(self.no_label_text)

    def slider_value_change_cb(self, event):
        nval = self.slider.get_value()
        self.value_label.set_text(str(nval) + self.unit)
        if self.on_value_change != None:
            self.on_value_change(nval)

    def slider_release_cb(self, event):
        nval = self.slider.get_value()
        self.on_slider_release(nval)

    def yes_btn_click_cb(self, event):
        nval = self.slider.get_value()
        if self.on_yes_clicked != None:
            self.on_yes_clicked(nval)
        self.exit(self.exit_anim)

    def no_btn_click_cb(self, event):
        if self.on_no_clicked != None:
            self.on_no_clicked(self.number_default)
        self.exit(self.exit_anim)
