import lvgl as lv

from . import Activity

class InfoActivity(Activity):
    def __init__(self, title, text, on_ok_clicked=None, ok_label_text='OK', exit_anim=None):
        self.title = title
        self.text = text
        self.on_ok_clicked = on_ok_clicked
        self.ok_label_text = ok_label_text
        self.exit_anim = exit_anim

    def setup(self):
        self.title_label = lv.label(self.scr)
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 30)
        self.title_label.set_width(160)
        self.title_label.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
        self.title_label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.title_label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.title_label.set_text(self.title)

        self.text_label = lv.label(self.scr)
        self.text_label.align(lv.ALIGN.CENTER, 0, 0)
        self.text_label.set_width(200)
        self.text_label.set_text(self.text)

        self.ok_btn = lv.button(self.scr)
        self.ok_btn.align(lv.ALIGN.BOTTOM_MID, 0, 0)
        self.ok_btn.set_size(240, 60)
        self.ok_btn.add_event_cb(self.ok_btn_click_cb, lv.EVENT.CLICKED, None)
        self.ok_btn_label = lv.label(self.ok_btn)
        self.ok_btn_label.align(lv.ALIGN.CENTER, 0, 0)
        self.ok_btn_label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok_btn_label.set_text(self.ok_label_text)

    def ok_btn_click_cb(self, event):
        if self.on_ok_clicked != None:
            self.on_ok_clicked()
        self.exit(self.exit_anim)
