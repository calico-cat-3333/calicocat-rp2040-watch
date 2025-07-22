# 编写应用程序
CCES 允许用户通过编写 Python 脚本来扩展其功能，每个应用程序通过一个 .py 文件来实现。下面是以蜂鸣器琴为例，从编写应用程序到安装到手表上的基本步骤：

## 创建文件

新建一个.py 文件，名称格式必须为 xxx_app.py，编辑文件，导入必须的组件和库，包括 LVGL、Activity 类和 AppMeta 类。

```
import lvgl as lv
from cces.appmgr import AppMeta
from cces.activity import Activity
# 蜂鸣器琴需要调用蜂鸣器的能力，故还需要导入 hal
from cces import hal
```

## 注册应用元数据

创建命名为 appmeta 的 AppMeta 实例，参数依次为应用名称，应用图标，应用主界面 Acitvity 类，系统启动时执行的函数。

```
appmeta = AppMeta('蜂鸣器琴', lv.SYMBOL.AUDIO, MainActivity)
```

第二个参数应用图标可以是 lv.SYMOBL.xxx 或者 lv.img_dsc_t (理论上说，任何 lv.image.set_scr() 函数可以接受的参数都可以) 。

第四个参数可选，如果应用不需要在系统启动时自动执行某些任务，则不需要。

## 编写主界面 Activity

继承 Activity 类创建主界面，重写 setup 函数，创建图形界面 （有需要也可以实现 \_\_init\_\_ 函数）。

```
class MainActivity(Activity):
    def __init__(self):
        self.btn_map = ['\n1', '\n2', '\n3', '\n4', '\n', '\n5', '\n6', '\n7', '.\n1', '']
        self.tones = (262, 294, 330, 349, 392, 440, 494, 523)  # C大调音阶

    def setup(self):
        self.keys = lv.buttonmatrix(self.scr)
        self.keys.align(lv.ALIGN.CENTER, 0, 0)
        self.keys.set_map(self.btn_map)
        self.keys.set_size(200, 150)
        self.keys.add_event_cb(self.bm_click_cb, lv.EVENT.VALUE_CHANGED, None)
        self.keys.set_style_border_side(lv.BORDER_SIDE.NONE, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.keys.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN | lv.STATE.DEFAULT)

        self.exit_btn = lv.button(self.scr)
        self.exit_btn.align(lv.ALIGN.BOTTOM_MID, 0, -10)
        self.exit_btn.add_event_cb(self.exit_btn_cb, lv.EVENT.CLICKED, None)
        self.exit_btn_label = lv.label(self.exit_btn)
        self.exit_btn_label.align(lv.ALIGN.CENTER, 0, 0)
        self.exit_btn_label.set_text('EXIT')

        self.title_label = lv.label(self.scr)
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 10)
        self.title_label.set_text('蜂鸣器琴')
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)
```

## 实现生命周期函数

按照需要重写 Activity 的关键生命周期函数。

`on_covered(self)`: 被新窗口覆盖时执行

`on_cover_exit(self)`: 覆盖窗口退出时执行

`before_exit(self)`: 退出前执行

`refresh_event_cb(self, event)`: 接收到刷新请求时执行，需要配合 `from cces.activity import REFRESHON`在 setup 函数中编写 `self.refresh_on=REFRESHON.XXX`

本例中，原本无需添加生命周期函数，作为演示，这里添加退出时发声功能。

```
class MainActivity(Activity):
    def __init__(self):
        self.btn_map = ['\n1', '\n2', '\n3', '\n4', '\n', '\n5', '\n6', '\n7', '.\n1', '']
        self.tones = (262, 294, 330, 349, 392, 440, 494, 523)  # C大调音阶

    def setup(self):
        self.keys = lv.buttonmatrix(self.scr)
        self.keys.align(lv.ALIGN.CENTER, 0, 0)
        self.keys.set_map(self.btn_map)
        self.keys.set_size(200, 150)
        self.keys.add_event_cb(self.bm_click_cb, lv.EVENT.VALUE_CHANGED, None)
        self.keys.set_style_border_side(lv.BORDER_SIDE.NONE, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.keys.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN | lv.STATE.DEFAULT)

        self.exit_btn = lv.button(self.scr)
        self.exit_btn.align(lv.ALIGN.BOTTOM_MID, 0, -10)
        self.exit_btn.add_event_cb(self.exit_btn_cb, lv.EVENT.CLICKED, None)
        self.exit_btn_label = lv.label(self.exit_btn)
        self.exit_btn_label.align(lv.ALIGN.CENTER, 0, 0)
        self.exit_btn_label.set_text('EXIT')

        self.title_label = lv.label(self.scr)
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 10)
        self.title_label.set_text('蜂鸣器琴')
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)

    def before_exit(self):
        hal.buzzer.beep(4000)
```

## 编写业务逻辑代码

按照需要编写业务逻辑代码。

```
class MainActivity(Activity):
    def __init__(self):
        self.btn_map = ['\n1', '\n2', '\n3', '\n4', '\n', '\n5', '\n6', '\n7', '.\n1', '']
        self.tones = (262, 294, 330, 349, 392, 440, 494, 523)  # C大调音阶

    def setup(self):
        self.keys = lv.buttonmatrix(self.scr)
        self.keys.align(lv.ALIGN.CENTER, 0, 0)
        self.keys.set_map(self.btn_map)
        self.keys.set_size(200, 150)
        self.keys.add_event_cb(self.bm_click_cb, lv.EVENT.VALUE_CHANGED, None)
        self.keys.set_style_border_side(lv.BORDER_SIDE.NONE, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.keys.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN | lv.STATE.DEFAULT)

        self.exit_btn = lv.button(self.scr)
        self.exit_btn.align(lv.ALIGN.BOTTOM_MID, 0, -10)
        self.exit_btn.add_event_cb(self.exit_btn_cb, lv.EVENT.CLICKED, None)
        self.exit_btn_label = lv.label(self.exit_btn)
        self.exit_btn_label.align(lv.ALIGN.CENTER, 0, 0)
        self.exit_btn_label.set_text('EXIT')

        self.title_label = lv.label(self.scr)
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 10)
        self.title_label.set_text('蜂鸣器琴')
        self.scr.add_event_cb(self.gesture_event_cb, lv.EVENT.GESTURE, None)

    def before_exit(self):
        hal.buzzer.beep(4000)

    def gesture_event_cb(self, event):
        lv.indev_active().wait_release()
        gesture = lv.indev_active().get_gesture_dir()
        if gesture == lv.DIR.RIGHT:
            self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)

    def bm_click_cb(self, _):
        n = self.keys.get_selected_button()
        hal.buzzer.beep(self.tones[n])

    def exit_btn_cb(self, _):
        self.exit(lv.SCR_LOAD_ANIM.OVER_RIGHT)
```

## 安装应用

将文件拷贝到手表文件系统的 apps 文件夹中，重启手表完成应用安装。也可放置在本储存库的 apps 文件夹中，这样可以在模拟器中使用。