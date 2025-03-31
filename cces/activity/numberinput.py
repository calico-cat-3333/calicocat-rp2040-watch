import lvgl as lv

from . import Activity

class NumberInputActivity(Activity):
    def __init__(self,
                 title,
                 number_min = -0xffffff,
                 number_max = 0xffffff,
                 on_ok_clicked = None,
                 ndefault = None,
                 isfloat = False,
                 exit_anim = None
                 ):
        # on_ok_clicked 需要接受一个参数，该参数为输入的数字
        self.title = title
        self.number_min = number_min
        self.number_max = number_max
        self.on_ok_clicked = on_ok_clicked
        self.number_default = ndefault
        self.isfloat = isfloat
        self.exit_anim = exit_anim

    def setup(self):
        self.title_label = lv.label(self.scr)
        self.title_label.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
        self.title_label.set_text(self.title)
        self.title_label.set_width(120)
        self.title_label.set_height(lv.SIZE_CONTENT)
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 20)

        self.keyboard = lv.keyboard(self.scr)
        self.custom_map = [
            '1', '2', '3', '0', lv.SYMBOL.BACKSPACE, '\n',
            '4', '5', '6', '.', '+/-', '\n',
            '7', '8', '9', lv.SYMBOL.LEFT, lv.SYMBOL.RIGHT, '\n',
            ' ', lv.SYMBOL.OK, lv.SYMBOL.CLOSE, ' ', ''
        ]

        self.ctrl_map = [
            2, 2, 2, 2, 2,
            2, 2, 2, 2, 2,
            2, 2, 2, 2, 2,
            1 | lv.buttonmatrix.CTRL.HIDDEN, 4 | lv.buttonmatrix.CTRL.NO_REPEAT, 4 | lv.buttonmatrix.CTRL.NO_REPEAT, 1 | lv.buttonmatrix.CTRL.HIDDEN,
        ]

        self.keyboard.set_map(self.keyboard.MODE.USER_1, self.custom_map, self.ctrl_map)
        self.keyboard.set_mode(self.keyboard.MODE.USER_1)
        self.keyboard.set_size(200, 140)
        self.keyboard.align(lv.ALIGN.CENTER, 0, 35)

        self.number_area = lv.textarea(self.scr)
        self.number_area.set_width(190)
        self.number_area.set_height(lv.SIZE_CONTENT)
        self.number_area.set_one_line(True)
        if self.number_default != None:
            self.number_area.set_text(str(self.number_default))
        self.number_area.align(lv.ALIGN.TOP_MID, 0, 45)
        self.number_area.add_event_cb(self.kb_ok_cb, lv.EVENT.READY, None)
        self.number_area.add_event_cb(self.kb_cancel_cb, lv.EVENT.CANCEL, None)
        self.number_area.set_placeholder_text(str(self.number_min) + '~' + str(self.number_max))
        self.number_area.add_state(lv.STATE.FOCUSED)

        self.keyboard.set_textarea(self.number_area)

    def kb_ok_cb(self, _):
        try:
            if self.isfloat:
                number = float(self.number_area.get_text())
            else:
                number = int(self.number_area.get_text())
        except:
            if self.number_default != None:
                self.number_area.set_text(str(self.number_default))
            else:
                self.number_area.set_text('')
            self.title_label.set_text(lv.SYMBOL.CLOSE + ' ' + self.title)
            return

        if number >= self.number_min and number <= self.number_max:
            if self.on_ok_clicked != None:
                self.on_ok_clicked(number)
            self.exit(self.exit_anim)
        else:
            if self.number_default != None:
                self.number_area.set_text(str(self.number_default))
            else:
                self.number_area.set_text('')
            self.title_label.set_text(lv.SYMBOL.CLOSE + ' ' + self.title)

    def kb_cancel_cb(self, _):
        self.exit(self.exit_anim)