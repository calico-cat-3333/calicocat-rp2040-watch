import lvgl as lv

from cces.appmgr import AppMeta
from cces.activity import Activity, REFRESHON, styles, fonts
from cces import hal, gadgetbridge

class MainActivity(Activity):
    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.refresh_on = REFRESHON.GB_MUSIC | REFRESHON.BLE_CONNECTION
        self.music_progress = lv.arc(self.scr)
        self.music_progress.set_size(225, 225)
        self.music_progress.align(lv.ALIGN.CENTER, 0, 0)
        self.music_progress.remove_flag(lv.obj.FLAG.CLICKABLE)
        self.music_progress.set_style_arc_width(5, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.music_progress.set_style_arc_width(5, lv.PART.INDICATOR | lv.STATE.DEFAULT)

        self.music_play = lv.button(self.scr)
        self.music_play.set_size(70, 70)
        self.music_play.align(lv.ALIGN.CENTER, 0, 0)
        self.music_play.set_style_radius(70, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.music_play.add_event_cb(self.music_play_cb, lv.EVENT.CLICKED, None)

        self.play_label = lv.label(self.music_play)
        self.play_label.align(lv.ALIGN.CENTER, 0, 0)
        self.play_label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.music_prev = lv.button(self.scr)
        self.music_prev.set_size(50, 50)
        self.music_prev.align(lv.ALIGN.CENTER, -70, 0)
        self.music_prev.add_style(styles.transparent_button, lv.PART.MAIN| lv.STATE.DEFAULT)
        self.music_prev.add_style(styles.white_button, lv.PART.MAIN | lv.STATE.PRESSED)
        self.music_prev.add_event_cb(lambda e: gadgetbridge.music_ctrl('previous'), lv.EVENT.CLICKED, None)

        self.prev_label = lv.label(self.music_prev)
        self.prev_label.set_text(lv.SYMBOL.PREV)
        self.prev_label.align(lv.ALIGN.CENTER, 0, 0)
        self.prev_label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.music_next = lv.button(self.scr)
        self.music_next.set_size(50, 50)
        self.music_next.align(lv.ALIGN.CENTER, 70, 0)
        self.music_next.set_style_bg_opa(0, lv.PART.MAIN| lv.STATE.DEFAULT)
        self.music_next.add_style(styles.transparent_button, lv.PART.MAIN| lv.STATE.DEFAULT)
        self.music_next.add_style(styles.white_button, lv.PART.MAIN | lv.STATE.PRESSED)
        self.music_next.add_event_cb(lambda e: gadgetbridge.music_ctrl('next'), lv.EVENT.CLICKED, None)

        self.next_label = lv.label(self.music_next)
        self.next_label.set_text(lv.SYMBOL.NEXT)
        self.next_label.align(lv.ALIGN.CENTER, 0, 0)
        self.next_label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.music_info = lv.label(self.scr)
        self.music_info.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
        self.music_info.set_text("TRACK - ARTIST - ALBUM")
        self.music_info.set_width(140)
        self.music_info.align(lv.ALIGN.CENTER, 0, -60)
        self.music_info.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.vol_up = lv.button(self.scr)
        self.vol_up.set_size(35, 35)
        self.vol_up.align(lv.ALIGN.CENTER, 35, 70)
        self.vol_up.add_style(styles.transparent_button, lv.PART.MAIN| lv.STATE.DEFAULT)
        self.vol_up.add_style(styles.white_button, lv.PART.MAIN | lv.STATE.PRESSED)
        self.vol_up.add_event_cb(lambda e: gadgetbridge.music_ctrl('volumeup'), lv.EVENT.CLICKED, None)

        self.vol_up_label = lv.label(self.vol_up)
        self.vol_up_label.set_text(lv.SYMBOL.VOLUME_MAX)
        self.vol_up_label.align(lv.ALIGN.CENTER, 0, 0)

        self.vol_down = lv.button(self.scr)
        self.vol_down.set_size(35, 35)
        self.vol_down.align(lv.ALIGN.CENTER, -35, 70)
        self.vol_down.add_style(styles.transparent_button, lv.PART.MAIN| lv.STATE.DEFAULT)
        self.vol_down.add_style(styles.white_button, lv.PART.MAIN | lv.STATE.PRESSED)
        self.vol_down.add_event_cb(lambda e: gadgetbridge.music_ctrl('volumedown'), lv.EVENT.CLICKED, None)

        self.vol_down_label = lv.label(self.vol_down)
        self.vol_down_label.set_text(lv.SYMBOL.VOLUME_MID)
        self.vol_down_label.align(lv.ALIGN.CENTER, 0, 0)

        self.refresh_event_cb(None)

    def music_play_cb(self, event):
        if self.state == 'play':
            gadgetbridge.music_ctrl('pause')
        elif self.state == 'pause':
            gadgetbridge.music_ctrl('play')

    def refresh_event_cb(self, event):
        if not hal.ble.connected():
            title_text = '蓝牙未连接'
        else:
            artist = gadgetbridge.music_info.get('artist', '?')
            track = gadgetbridge.music_info.get('track', '?')
            album = gadgetbridge.music_info.get('album', '?')
            title_text = track + ' - ' + artist + ' - ' + album
        if self.music_info.get_text() != title_text:
            self.music_info.set_text(title_text)
        dur = gadgetbridge.music_info.get('dur', 0xffff)
        self.music_progress.set_range(0, dur)
        position = gadgetbridge.music_state.get('position', 0)
        self.music_progress.set_value(position)
        self.state = gadgetbridge.music_state.get('state', 'pause')
        if self.state == 'pause':
            self.play_label.set_text(lv.SYMBOL.PLAY)
        elif self.state == 'play':
            self.play_label.set_text(lv.SYMBOL.PAUSE)

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.RIGHT:
            self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

appmeta = AppMeta('音乐控制', fonts.SYMBOL.DISC, MainActivity)