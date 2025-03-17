import lvgl as lv

from . import Activity

class InfoActivity(Activity):
    def __init__(self, title, text, on_ok_clicked=None, ok_label_text='OK'):
        self.title = title
        self.text = text
        self.on_ok_clicked = on_ok_clicked
        self.ok_label_text = ok_label_text

    def setup(self):
        self.title_label = lv.label(self.scr)
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 40)
        self.title_label.set_style_text_font(lv.font_montserrat_24, 0)
        self.title_label.set_text(self.title)

        self.text_label = lv.label(self.scr)
        self.text_label.align(lv.ALIGN.CENTER, 0, -20)
        self.text_label.set_text(self.text)

        self.ok_btn = lv.button(self.scr)
        self.ok_btn.align(lv.ALIGN.BOTTOM_MID, 0, -15)
        self.ok_btn.add_event_cb(self.ok_btn_click_cb, lv.EVENT.CLICKED, None)
        self.ok_btn_label = lv.label(self.ok_btn)
        self.ok_btn_label.set_style_text_font(lv.font_montserrat_24, 0)
        self.ok_btn_label.set_text(self.ok_label_text)

    def ok_btn_click_cb(self, event):
        if self.on_ok_clicked != None:
            self.on_ok_clicked()
        self.exit()
