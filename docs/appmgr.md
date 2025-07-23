# `appmgr` - AppManager

负责加载和管理应用程序，提供 Launcher UI

## AppMeta(self, name, icon, main_activity, on_system_start_cb=None) 类

App 元数据，描述 App 的基本信息。

参数 name 为应用名称字符串。

参数 icon 为应用图标，可以是 lv.SYMOBL.xxx 或者 lv.img_dsc_t (理论上说，任何 lv.image.set_scr() 函数可以接受的参数都可以) 大小暂定 20x20 px.

参数 main_activity 为应用主页 Acitvit 类，注意是类，不是实例。

参数 on_system_start_cb 为可调用对象或 None，在系统启动时执行，可以用于初始化全局任务等等。

## launch_app(name, anim=None)

使用应用名称加载该应用。

参数 name 为应用名称字符串。

参数 anim 为动画，请参考 lv_screen_load_anim_t 文档。（注意：C 转写成 micropython 如下：`LV_SCR_LOAD_ANIM_MOVE_LEFT` 对应 `lv.SCR_LOAD_ANIM.MOVE_LEFT`）