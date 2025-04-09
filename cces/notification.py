import time
import lvgl as lv

from .activity import Activity, REFRESHON, refresh_activity_on, styles, current_activity
from . import hal, powermanager
from . import settingsdb

class NotificationCenter(Activity): # 通知中心
    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.refresh_on = self.refresh_on | REFRESHON.NOTIFICATION
        self.scr.remove_flag(lv.obj.FLAG.SCROLLABLE)

        self.notify_remove = lv.button(self.scr)
        self.notify_remove.set_size(40, 140)
        self.notify_remove.align(lv.ALIGN.RIGHT_MID, 0, 0)
        self.notify_remove.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.notify_remove.add_event_cb(self.notify_remove_cb, lv.EVENT.CLICKED, None)

        self.notify_remove_label = lv.label(self.notify_remove)
        self.notify_remove_label.set_text(lv.SYMBOL.TRASH)
        self.notify_remove_label.align(lv.ALIGN.LEFT_MID, 0, 0)
        self.notify_remove_label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.notify_next = lv.button(self.scr)
        self.notify_next.set_size(240, 50)
        self.notify_next.align(lv.ALIGN.TOP_MID, 0, 0)
        self.notify_next.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.notify_next.add_style(styles.white_button, lv.PART.MAIN| lv.STATE.DEFAULT)
        self.notify_next.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.notify_next.set_style_border_width(2, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.notify_next.set_style_border_color(lv.color_hex(0xDDDDDD), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.notify_next.add_event_cb(self.notify_next_cb, lv.EVENT.CLICKED, None)

        self.notify_title = lv.label(self.notify_next)
        self.notify_title.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
        self.notify_title.set_text("NotificationTitle")
        self.notify_title.set_width(120)
        self.notify_title.align(lv.ALIGN.BOTTOM_MID, 0, 0)
        self.notify_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.notify_prev = lv.button(self.scr)
        self.notify_prev.set_size(240, 50)
        self.notify_prev.align(lv.ALIGN.BOTTOM_MID, 0, 0)
        self.notify_prev.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.notify_prev.add_style(styles.white_button, lv.PART.MAIN| lv.STATE.DEFAULT)
        self.notify_prev.set_style_border_side(lv.BORDER_SIDE.TOP, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.notify_prev.set_style_border_width(2, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.notify_prev.set_style_border_color(lv.color_hex(0xDDDDDD), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.notify_prev.add_event_cb(self.notify_prev_cb, lv.EVENT.CLICKED, None)

        self.notify_number = lv.label(self.notify_prev)
        self.notify_number.set_text("--/--")
        self.notify_number.align(lv.ALIGN.TOP_MID, 0, 0)

        self.notify_text = lv.textarea(self.scr)
        self.notify_text.set_size(180, 130)
        self.notify_text.set_text("")
        self.notify_text.set_placeholder_text("Empty...")
        self.notify_text.align(lv.ALIGN.CENTER, -15, 0)
        self.notify_text.remove_flag(lv.obj.FLAG.CLICK_FOCUSABLE)
        self.notify_text.set_cursor_pos(0)
        self.notify_text.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.notify_text.set_style_border_side(lv.BORDER_SIDE.NONE, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.notify_text.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN | lv.STATE.DEFAULT)

        self.current_notify = len(_notify_id_list) - 1
        self.update_display()

    def show_latest(self):
        self.current_notify = len(_notify_id_list) - 1
        self.update_display()

    def gesture_event_cb(self, _):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.TOP:
            self.notify_prev_cb()
        if gesture == lv.DIR.BOTTOM:
            self.notify_next_cb()
        if gesture == lv.DIR.LEFT:
            self.notify_remove_cb()

    def refresh_event_cb(self, _):
        if self.current_notify > len(_notify_id_list) - 1:
            self.current_notify = len(_notify_id_list) - 1
        self.update_display()

    def update_display(self):
        if self.current_notify == -1:
            title = '通知中心'
            text = '没有更多通知'
            if len(_notify_id_list) != 0:
                text = text + '\n点击按钮或左划以清空全部'
        else:
            nid = _notify_id_list[self.current_notify]
            notify = _notify_storage.get(nid)
            title = notify['title']
            sendtime = time.localtime(notify['time'])
            text = '{:0>4d}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}\n'.format(*sendtime[:5]) + notify['text']
        self.notify_title.set_text(title)
        self.notify_text.set_text(text)
        self.notify_text.set_cursor_pos(0)
        self.notify_text.scroll_to_y(0, False)
        self.notify_number.set_text(str(self.current_notify + 1) + '/' + str(len(_notify_id_list)))

    def notify_next_cb(self, *args):
        if self.current_notify >= 0:
            self.current_notify = self.current_notify - 1
            self.update_display()

    def notify_prev_cb(self, *args):
        if self.current_notify < len(_notify_id_list) - 1:
            self.current_notify = self.current_notify + 1
            self.update_display()
        else:
            self.exit(lv.SCR_LOAD_ANIM.OVER_TOP)

    def notify_remove_cb(self, *args):
        if self.current_notify >= 0:
            remove(_notify_id_list[self.current_notify], False)
            self.current_notify = self.current_notify - 1
        elif self.current_notify == -1:
            self.current_notify = -1
            clear_all(False)
        self.update_display()

    def on_covered(self):
        self.exit()
        # 需要特殊处理，不然会出问题
        current_activity().on_covered()

_notify_storage = {}
_notify_id_list = []
_notify_id_max = 0

def _new_nid():
    # 生成一个新的通知 id
    # 特殊之处： gadgetbridge 程序产生的通知的 id 为正数，其他为负数，因为 gadgetbridge 使用自己的通知 id
    global _notify_id_max
    _notify_id_max = _notify_id_max - 1
    return _notify_id_max

def send(title, text, nid=None, *, popup=False):
    # send a Notification
    # return notification id
    # beep when dnd is off
    # nid is only for gadgetbridge
    notify = {'title':title, 'text':text, 'time':time.time()}
    if nid == None:
        nid = _new_nid()
    if nid in _notify_id_list:
        return None
    _notify_id_list.append(nid)
    _notify_storage[nid] = notify
    if not settingsdb.get('do_not_disturb', False):
        hal.buzzer.beep()
    refresh_activity_on(REFRESHON.NOTIFICATION)
    if popup:
        powermanager.try_wakeup()
        c = current_activity()
        if isinstance(c, NotificationCenter):
            c.show_latest()
        else:
            NotificationCenter().launch()
    return nid

def remove(nid, need_refresh=True):
    if nid in _notify_id_list:
        _notify_id_list.remove(nid)
        _notify_storage.pop(nid)
        if need_refresh:
            refresh_activity_on(REFRESHON.NOTIFICATION)

def clear_all(need_refresh=True):
    _notify_id_list.clear()
    _notify_storage.clear()
    if need_refresh:
        refresh_activity_on(REFRESHON.NOTIFICATION)