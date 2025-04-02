import os
import sys
import gc
import lvgl as lv

from .log import log, ERROR
from .activity import Activity

APP_PATH = '/apps'
if sys.platform != 'rp2':
    APP_PATH = 'apps'

app_list = []

# 如果一个 .py 文件或文件夹是一个 app，则必须包含类似 appmeta = AppMeta('appname', lv.SYMBOL.WIFI, MainActivity) 的内容并保证在 import 此文件时该语句可以执行，.py 文件或文件夹必须以 _app 为结尾 如 muyu_app.py musicctrl_app
class AppMeta:
    def __init__(self, name, icon, main_activity, on_system_start_cb=None):
        # name：应用名称字符串
        # icon：应用图标，可以是 lv.SYMOBL.xxx 或者 lv.img_dsc_t (理论上说，任何 lv.image.set_scr() 函数可以接受的参数都可以) 大小暂定 20x20 px
        # main_activity：应用主页 Acitvit 类，注意是类，不是实例
        # on_system_start_cb：函数回调，在系统启动时执行，可以用于初始化全局任务等等
        self.name = name
        self.icon = icon
        self.main_activity = main_activity
        self.on_system_start_cb = on_system_start_cb
        log('app', self.name, 'load.')
        app_list.append(self)

    def start(self, *args):
        self.main_activity().launch(lv.SCR_LOAD_ANIM.OVER_LEFT)

    def on_system_start(self):
        if self.on_system_start_cb != None:
            self.on_system_start_cb()

class Launcher(Activity):
    def __init__(self):
        pass

    def setup(self):
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
        self.applist = lv.list(self.scr)
        self.applist.set_size(200, 220)
        self.applist.align(lv.ALIGN.CENTER, 20, 0)
        self.applist.set_style_border_side(lv.BORDER_SIDE.NONE, lv.PART.MAIN | lv.STATE.DEFAULT)

        for app in app_list:
            btn = self.applist.add_button(app.icon, app.name)
            btn.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.SPACE_EVENLY)
            btn.add_event_cb(lambda event, app=app: self.list_obj_click(event, app), lv.EVENT.CLICKED, None)
            btn.set_style_pad_ver(15, lv.PART.MAIN | lv.STATE.DEFAULT)
            img = btn.get_child(0)
            img.set_width(20)
            img.set_inner_align(lv.image.ALIGN.CENTER)

        self.exit_btn = lv.button(self.scr)
        self.exit_btn.align(lv.ALIGN.LEFT_MID, 0, 0)
        self.exit_btn.set_size(40, 240)
        self.exit_btn.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.exit_btn.add_event_cb(self.exit_btn_cb, lv.EVENT.CLICKED, None)
        self.exit_btn_label = lv.label(self.exit_btn)
        self.exit_btn_label.set_text(lv.SYMBOL.LEFT)
        self.exit_btn_label.align(lv.ALIGN.RIGHT_MID, 0, 0)
        self.exit_btn_label.set_style_text_font(lv.font_montserrat_24, 0)

    def exit_btn_cb(self, event):
        self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.RIGHT:
            self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

    def list_obj_click(self, event, app):
        app.start()
        self.exit()

def load_apps():
    if len(app_list) != 0:
        return
    for afile in os.ilistdir(APP_PATH):
        fname = afile[0]
        ftype = afile[1]
        if fname.endswith('_app.py') and len(fname) > 6 and ftype & 0xf000 == 0x8000:
            # signal py file app
            appname = 'apps.' + fname[:-3]
            log('find apps/' + fname, 'will load')
        elif fname.endswith('_app') and len(fname) > 3 and ftype & 0xf000 == 0x4000 and '__init__.py' in os.listdir(APP_PATH + '/' + fname):
            # app with more filse
            appname = 'apps.' + fname
            log('find apps/' + fname, 'will load')
        else:
            log('file apps/', fname, 'not a app')
            continue

        try:
            exec('import ' + appname)
        except Exception as e:
            log('faild in loading', appname, e, level=ERROR, exc=e)
            continue

    for app in app_list:
        app.on_system_start()