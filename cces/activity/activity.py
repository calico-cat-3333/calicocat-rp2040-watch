import lvgl as lv

from ..log import log

# 正在显示的 activity
# 堆栈的形式
# 栈底元素是系统启动之后的第一个 activity 通常是表盘，他将永远不会退出
activity_stack = []

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

        if len(activity_stack) != 0:
            activity_stack[-1].on_covered()

        activity_stack.append(self)
        if anim != None:
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
        if len(activity_stack) == 0:
            # 如果这是最后一个 activity 不能退出
            return
        log(str(self.__class__), 'exit')
        self.before_exit()
        activity_stack.pop()
        activity_stack[-1].on_cover_exit()
        if anim != None:
            lv.screen_load_anim(activity_stack[-1].scr, anim, 200, 0, True)
        else:
            lv.screen_load(activity_stack[-1].scr)
            self.scr.delete()