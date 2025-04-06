import lvgl as lv
from micropython import const
import time

from cces.appmgr import AppMeta
from cces.activity import Activity, fonts, REFRESHON
from cces import hal, gadgetbridge

_TIMEOUT = const(12 * 60 * 60) # 超过 12 个小时的数据被认为无效
_WEATHER_ICON_MAP = (fonts.SYMBOL.CLOUD_BOLT, fonts.SYMBOL.RAIN, '?', fonts.SYMBOL.HEAVY_RAIN, fonts.SYMBOL.SNOW, fonts.SYMBOL.SMOG, fonts.SYMBOL.CLOUD) # 通用图标对照表，仅根据最高位进行解析，然后特殊情况特殊处理
_WIND_DIRS = ('北风', '东北风', '东风', '东南风', '南风', '西南风', '西风', '西北风') # 风向查找表

# 背景主颜色  背景副颜色  字体颜色        情况
_BG_COLOR_MAP = (
    (0xFFC107, 0xFF9800, 0xFFFFFF),  # 0: 晴天白天
    (0x001A43, 0x141B2C, 0xFFFFFF),  # 1: 晴天夜间
    (0xB3E5FC, 0x03A9F4, 0x000000),  # 2: 阴天1(801,802)白天
    (0x98B2C8, 0x1E76BB, 0x000000),  # 3: 阴天2(803,804)白天
    (0x13243E, 0x1C212C, 0xFFFFFF),  # 4: 阴天夜间
    (0x448AFF, 0x3F51B5, 0xFFFFFF),  # 5: 雨天白天
    (0x13243E, 0x1C212C, 0xFFFFFF),  # 6: 雨天夜间（同阴天夜间）
    (0x6CB9FF, 0x4E7DBD, 0x000000),  # 7: 雪天白天
    (0x2D4A63, 0x1A2A40, 0xFFFFFF),  # 8: 雪天夜间
    (0x2F2F4F, 0x1A2A40, 0xFFFF00),  # 9: 雷暴天气（昼夜同）
    (0xB4A784, 0x786F57, 0x000000),  # 10: 雾霾/沙尘白天
    (0x3F3B31, 0x28241A, 0xFFFFFF),  # 11: 雾霾/沙尘夜间
    (0x520606, 0x2C0505, 0xFFFFFF),  # 12: 极端（狂风/龙卷风）
)

class MainActivity(Activity):
    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.refresh_on = REFRESHON.GB_WEATHER

        self.scr.set_style_bg_color(lv.color_hex(0xB3E5FC), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.scr.set_style_bg_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT)
        self.scr.set_style_bg_grad_color(lv.color_hex(0x03A9F4), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.scr.set_style_bg_grad_dir(lv.GRAD_DIR.VER, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.location = lv.label(self.scr)
        self.location.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
        self.location.set_width(80)
        self.location.align(lv.ALIGN.TOP_MID, 0, 10)
        self.location.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.location.set_style_text_font(lv.font_extra_symbols, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.current_temp = lv.label(self.scr)
        self.current_temp.set_text('--°C')
        self.current_temp.align(lv.ALIGN.CENTER, 0, -50)
        self.current_temp.set_style_text_font(lv.font_number72, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.weather_info = lv.label(self.scr)
        self.weather_info.set_size(200, 125)
        self.weather_info.align(lv.ALIGN.TOP_MID, 0, 115)
        self.weather_info.set_style_text_font(lv.font_extra_symbols, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.weather_info.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.weather_info.set_style_radius(15, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.weather_info.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.weather_info.set_style_bg_opa(200, lv.PART.MAIN| lv.STATE.DEFAULT)
        self.weather_info.set_style_pad_top(5, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.refresh_event_cb(0)

    def refresh_event_cb(self, _):
        if time.time() - gadgetbridge.weather_data.get('time', 0) > _TIMEOUT:
            self.current_temp.set_text('--°C')
            self.location.set_text(fonts.SYMBOL.GPS + ' ?')
            self.weather_info.set_text('无有效天气信息\n请连接手机并更新天气')
            return

        temp_h = gadgetbridge.weather_data.get('hi', 0)
        temp_l = gadgetbridge.weather_data.get('lo', 0)
        code = gadgetbridge.weather_data.get('code', 0)
        wind = gadgetbridge.weather_data.get('wind', 0)
        wdir = gadgetbridge.weather_data.get('wdir', 0)
        ts = time.localtime(gadgetbridge.weather_data.get('time', 0))

        self.code2style(code)

        self.location.set_text(fonts.SYMBOL.GPS + ' ' + gadgetbridge.weather_data.get('loc', '?'))
        self.current_temp.set_text('{:d}°C'.format(gadgetbridge.weather_data.get('temp', 0) - 273))

        info_text = self.code2icon(code) + ' {}\n'.format(gadgetbridge.weather_data.get('txt', '')) + \
                    fonts.SYMBOL.TEMP_LOW + ' {:d}°C ~ '.format(temp_l - 273) + \
                    fonts.SYMBOL.TEMP_HIGH + ' {:d}°C\n'.format(temp_h - 273) + \
                    fonts.SYMBOL.FAN + ' {}  {:.1f}KM/h\n'.format(self.wdir2str(wdir), wind) + \
                    fonts.SYMBOL.WATER_DROP + ' {:d}%  '.format(gadgetbridge.weather_data.get('hum', 0)) + \
                    fonts.SYMBOL.RAIN + ' {:d}%\n'.format(gadgetbridge.weather_data.get('rain', 0)) + \
                    fonts.SYMBOL.SUN + 'UV {}\n'.format(gadgetbridge.weather_data.get('uv', 0)) + \
                    fonts.SYMBOL.CLOCK + ' {:0>2d}:{:0>2d}'.format(*ts[3:5])
        self.weather_info.set_text(info_text)

    def code2icon(self, code):
        # 参考 https://openweathermap.org/weather-conditions
        h = (code // 100) - 2
        isday = time.localtime()[3] >= 6 and time.localtime()[3] <= 18
        if h >= 0 and h <= 6:
            icon = _WEATHER_ICON_MAP[h]
        else:
            icon = '?'
        if code == 511: # 冻雨
            icon = fonts.SYMBOL.SNOW
        elif code == 771: # 狂风
            icon = fonts.SYMBOL.WIND
        elif code == 781: # 龙卷风
            icon = fonts.SYMBOL.TORNADO
        elif code == 800: # 晴
            icon = fonts.SYMBOL.SUN if isday else fonts.SYMBOL.MOON
        return icon

    def code2style(self, code):
        # 根据天气代码设置 GUI 背景和文字颜色
        h = (code // 100)
        isday = time.localtime()[3] >= 6 and time.localtime()[3] <= 18
        scs = (0xF5F5F5, 0xF5F5F5, 0x000000)
        if h == 2: # 雷暴
            scs = _BG_COLOR_MAP[9]
        elif h == 3 or h == 5: # 雨
            scs = _BG_COLOR_MAP[5] if isday else _BG_COLOR_MAP[6]
        elif h == 6: # 雪
            scs = _BG_COLOR_MAP[7] if isday else _BG_COLOR_MAP[8]
        elif h == 7: # 雾霾/沙尘暴等和极端天气
            if code == 771 or code == 781: # 极端天气
                scs = _BG_COLOR_MAP[12]
            else: # 雾霾/沙尘暴等
                scs = _BG_COLOR_MAP[10] if isday else _BG_COLOR_MAP[11]
        else:
            if code == 800: # 晴天
                scs = _BG_COLOR_MAP[0] if isday else _BG_COLOR_MAP[1]
            elif code == 801 or code == 802:
                scs = _BG_COLOR_MAP[2] if isday else _BG_COLOR_MAP[4]
            elif code == 803 or code == 804:
                scs = _BG_COLOR_MAP[3] if isday else _BG_COLOR_MAP[4]
        self.scr.set_style_bg_color(lv.color_hex(scs[0]), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.scr.set_style_bg_grad_color(lv.color_hex(scs[1]), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.location.set_style_text_color(lv.color_hex(scs[2]), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.current_temp.set_style_text_color(lv.color_hex(scs[2]), lv.PART.MAIN | lv.STATE.DEFAULT)

    def wdir2str(self, wdir):
        # 解析风向，原始数据是以正南方为 0 度，顺时针旋转的角度
        return _WIND_DIRS[int((wdir + 22.5) % 360 // 45)]

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.RIGHT:
            self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

appmeta = AppMeta('天气', fonts.SYMBOL.CLOUD, MainActivity)