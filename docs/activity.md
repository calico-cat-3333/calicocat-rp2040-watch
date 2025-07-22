# Activity

这里参考安卓系统 Activity 的概念，设计了 Activity 系统，CCES 的每个单独的界面都是 Activity, 由此实现对界面的统一管理。

我们通过类和继承来实现 Activity：每个界面都需要继承 Activity, 然后实现 setup \_\_init\_\_ on_covered 等关键函数，这些函数会绘制界面并在特定条件下执行。与 Activity 相关的业务逻辑也需要在该类中实现。

通过 `Activity().launch()` 可以启动 Activity, 在 Activity 内调用 self.exit() 可以退出 Activity, 退出后，Activity 实例自动销毁。

同时提供预先设计的几个 Activity 模板, 例如 InfoActivity 用于弹出提示信息，以便使用。

## Activity 类

基础 Activity 类。

### scr

本 Activity 的 LVGL screen. setup() 函数中，将组建创建函数的父控件设置为 `self.scr` 即可在该 Activity 上绘制控件。

### __init__(self)

可自由重写。

构造函数，用于实现创建实例时传递参数。

### setup(self)

需要重写。

界面加载时运行一次，重写该函数，在这里放置界面绘制相关的代码，代码中可以使用 `self.scr` 作为父控件。

特殊的，可以在这里写 `self.sidekey_exit = False` 以禁用侧键返回

写 `self.refresh_on = REFRESHON.XXX` 实现在特定条件下刷新，可以使用 | 组合多个条件，例如：

```
self.refresh_on = REFRESHON.GB_MUSIC | REFRESHON.BLE_CONNECTION
```

表示在 Gadgetbridge 音乐状态更新、蓝牙连接状态更新时刷新。

默认 `self.refresh_on = REFRESHON.NONE`

### on_covered(self)

按需重写。

本 Activity 被另一个覆盖时执行。

### on_cover_exit(self)

按需重写。

覆盖本 Activity 的 Activity 退出时执行。

### before_exit(self)

按需重写。

在本 Activity 退出时执行。

### refresh_event_cb(self, event)

按需重写。

接收到刷新请求时执行，刷新请求就是 setup 中添加的 `self.refresh_on = REFRESHON.XXX`。

### launch(self, anim=None)

不可重写。

启动当前 Activity.

参数 anim 为动画，请参考 lv_screen_load_anim_t 文档。（注意：C 转写成 micropython 如下：`LV_SCR_LOAD_ANIM_MOVE_LEFT` 对应 `lv.SCR_LOAD_ANIM.MOVE_LEFT`）

### exit(self, anim=None)

不可重写。

退出当前 Activity.

参数 anim 为动画，请参考 lv_screen_load_anim_t 文档。（注意：C 转写成 micropython 如下：`LV_SCR_LOAD_ANIM_MOVE_LEFT` 对应 `lv.SCR_LOAD_ANIM.MOVE_LEFT`）

## current_activity()

返回当前 Activity

## refresh_current_activity()

刷新当前 Activity, 除非 `self.refresh_on = REFRESHON.NONE`（注意：这是默认行为）

## refresh_activity_on(cond)

在特定条件下发送刷新当前 Activity

参数 `cond` 是 `REFRESHON`

## REFRESHON 枚举

在何种情况下刷新。

| 名称 |  描述   |
|--------------------|--------------------|
| `NONE` | 无论如何，都不刷新。 |
| `NOTIFICATION` | 通知发送或删除。 |
| `BLE_CONNECTION` | 蓝牙连接状态变化。 |
| `ZERO_CLOCK` | 每天 0 点。 |
| `GB_MUSIC` | 接收到来自 Gadgetbridge 的音乐状态。 |
| `GB_WEATHER` | 接收到来自 Gadgetbridge 的天气信息。|

## _ANIM_ENABLE 全局变量

开关，用于全局禁用 Activity 切换动画，目前仅能在开发过程中修改。

## 内置通用 Activity 模板

提供一系列常用功能的 Activity 模板。

### AskYesNoActivity(self, title, text, on_yes_clicked = None, on_no_clicked = None, yes_label_text = 'Yes', no_label_text = 'No', exit_anim = None)

询问是或否。

参数 title 和 text 都是字符串，分别是询问标题和正文，标题必须只有字母数字和符号。

参数 on_yes_clicked 和 on_no_clicked 都是可调用对象或 None，分别在是和否按钮点击后调用。

参数 yes_label_text 和 no_label_text 都是字符串，分别表示是和否按钮上的文字，必须只有字母数字和符号。

参数 exit_anim 为退出动画，请参考 lv_screen_load_anim_t 文档。（注意：C 转写成 micropython 如下：`LV_SCR_LOAD_ANIM_MOVE_LEFT` 对应 `lv.SCR_LOAD_ANIM.MOVE_LEFT`）

### InfoActivity(self, title, text, on_ok_clicked=None, ok_label_text='OK', exit_anim=None)

显示一条信息。

参数 title 和 text 都是字符串，分别是信息标题和正文，标题必须只有字母数字和符号。

参数 on_ok_clicked 是可调用对象或 None，在确定按钮点击后调用。

参数 ok_label_text 是字符串，是确定按钮上的文字，必须只有字母数字和符号。

参数 exit_anim 为退出动画，请参考 lv_screen_load_anim_t 文档。（注意：C 转写成 micropython 如下：`LV_SCR_LOAD_ANIM_MOVE_LEFT` 对应 `lv.SCR_LOAD_ANIM.MOVE_LEFT`）

### NumberInputActivity(self, title, number_min = -0xffffff, number_max = 0xffffff, on_ok_clicked = None, ndefault = None, isfloat = False, exit_anim = None)

向用户请求输入一个数字。

参数 title 是字符串，是标题，必须只有字母数字和符号。

参数 number_min, number_max 和 ndefault 是数字，分别表示可接受的最小值、最大值和默认值，默认值为 None 表示无默认值。

参数 on_ok_clicked 是可调用对象或 None，在确定按钮点击后调用。如果为可调用对象，需要接受一个参数，该参数将是用户输入的数字。

参数 isfloat 是布尔类型，表示是否接受浮点数输入。

参数 exit_anim 为退出动画，请参考 lv_screen_load_anim_t 文档。（注意：C 转写成 micropython 如下：`LV_SCR_LOAD_ANIM_MOVE_LEFT` 对应 `lv.SCR_LOAD_ANIM.MOVE_LEFT`）

### SliderActivity(self, title, number_min = 0, number_max = 100, number_default = 0, unit = '', on_yes_clicked = None, on_no_clicked = None, on_slider_release = None, on_value_change = None, step = 1, yes_label_text = 'Yes', no_label_text = 'No', exit_anim = None)

向用户请求使用滑块输入一个数字，并可以根据滑块位置随时响应。

参数 title 是字符串，是标题，必须只有字母数字和符号。

参数 number_min, number_max 和 number_default 是数字，分别表示可接受的最小值、最大值和默认值。

参数 unit 是字符串，表示单位，将显示在界面上。

参数 on_no_clicked 是可调用对象或 None，在否按钮点击后调用。如果为可调用对象，需要接受一个参数，该参数将是 number_default。

参数 on_yes_clicked, on_slider_release 和 on_value_change 都是可调用对象或 None，分别在是按钮点击、松开滑块、滑块值改变时调用。如果为可调用对象，需要接受一个参数，该参数将是滑块的当前值。

参数 step 为数字，是滑块滑动的步进值。

参数 yes_label_text 和 no_label_text 都是字符串，分别表示是和否按钮上的文字，必须只有字母数字和符号。

参数 exit_anim 为退出动画，请参考 lv_screen_load_anim_t 文档。（注意：C 转写成 micropython 如下：`LV_SCR_LOAD_ANIM_MOVE_LEFT` 对应 `lv.SCR_LOAD_ANIM.MOVE_LEFT`）