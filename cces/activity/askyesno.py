import lvgl as lv

from . import Activity

class AskYesNoActivity(Activity):
    def __init__(self, title, text, on_yes_clicked=None, on_no_clicked=None, yes_label_text='Yes', no_label_text='No'):
        self.title = title
        self.text = text
        self.on_yes_clicked = on_yes_clicked
        self.on_no_clicked = on_no_clicked
        self.yes_label_text = yes_label_text
        self.no_label_text = no_label_text

    def setup(self):
        self.title_label = lv.label(self.scr)
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 30)
        self.title_label.set_width(160)
        self.title_label.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
        self.title_label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.title_label.set_text(self.title)

        self.text_label = lv.label(self.scr)
        self.text_label.align(lv.ALIGN.CENTER, 0, 0)
        self.text_label.set_width(200)
        self.text_label.set_text(self.text)

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


    def yes_btn_click_cb(self, event):
        if self.on_yes_clicked != None:
            self.on_yes_clicked()
        self.exit()

    def no_btn_click_cb(self, event):
        if self.on_no_clicked != None:
            self.on_no_clicked()
        self.exit()
