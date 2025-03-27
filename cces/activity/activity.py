import gc
import lvgl as lv
from micropython import const

from ..log import log

# 正在显示的 activity
# 堆栈的形式
# 栈底元素是系统启动之后的第一个 activity 通常是表盘，他将永远不会退出
_activity_stack = []

_ANIM_ENABLE = const(True)

class Activity:
    def __init__(self):
        # 构造函数，在这里可以传递部分变量
        pass

    def setup(self):
        # 这里完成 GUI 构建
        pass

    def launch(self, anim=None):
        log(str(self.__class__), 'launch')
        self.scr = lv.obj()
        self.setup()

        if len(_activity_stack) != 0:
            _activity_stack[-1].on_covered()

        _activity_stack.append(self)
        if _ANIM_ENABLE and anim != None:
            lv.screen_load_anim(self.scr, anim, 200, 0, False)
        else:
            lv.screen_load(self.scr)


    def on_covered(self):
        # 当此 activity 被另一个覆盖时执行
        pass

    def on_cover_exit(self):
        # 当覆盖它的 activity 退出时执行
        pass

    def before_exit(self):
        # 退出前执行
        pass

    def exit(self, anim=None):
        if len(_activity_stack) == 0:
            # 如果这是最后一个 activity 不能退出
            return
        log(str(self.__class__), 'exit')
        self.before_exit()
        if self != _activity_stack[-1]:
            # 处理被覆盖的后台 Activity 退出
            _activity_stack.remove(self)
            self.scr.delete()
            gc.collect()
            return
        _activity_stack.pop()
        _activity_stack[-1].on_cover_exit()
        if _ANIM_ENABLE and anim != None:
            lv.screen_load_anim(_activity_stack[-1].scr, anim, 200, 0, True)
        else:
            lv.screen_load(_activity_stack[-1].scr)
            self.scr.delete()
        gc.collect()

def current_activity():
    # get current activity, None if no any activity
    if len(_activity_stack) != 0:
        return _activity_stack[-1]
    return None

def refresh_current_activity():
    # send LV_EVENT_REFRESH to current activity
    if len(_activity_stack) == 0:
        return
    _activity_stack[-1].scr.send_event(lv.EVENT.REFRESH, None)