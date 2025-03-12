from _uasyncio import TaskQueue
from _uasyncio import Task as _Task
from time import ticks_ms, ticks_add, ticks_diff
from micropython import const

# 简单的任务调度器，参考了 kmk_firmware 项目中使用的任务调度器
# 利用 _usyncio 中的 TaskQueue 配对堆实现
# 这些内容原本是为了 uasyncio 模块服务的，所以没有良好的文档记录
# 系统核心，任务调度有它负责
# lvgl 事件相关的调度由 lvgl 的 event_loop 调度器负责，那个调度器使用中断完成调度，与这里不冲突。

# 任务队列
_task_queue = TaskQueue()

# 标记，表示任务主动退出
TASKEXIT = const(11)

# 任务
class Task:
    def __init__(self, func, period, oneshot = False):
        self.func = func # 要运行的函数
        self._task = _Task(self.run)
        self.enabled = False
        self.period = period # 运行间隔，毫秒
        self.oneshot = oneshot # 仅运行一次
        self.args = ()
        self.kwargs = {}

    def start(self):
        self.enabled = True
        _task_queue.push(self._task, ticks_add(ticks_ms(), self.period))

    def set_args(*args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def start_with_arg(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.start()

    def stop(self):
        self.enabled = False
        # _task_queue.remove(self._task)

    def run(self):
        if not self.enabled:
            return
        r = self.func(*self.args, **self.kwargs)
        if (not self.oneshot) and r != TASKEXIT: # 如果 self.func 返回了 11 表示任务主动退出
            _task_queue.push(self._task, ticks_add(ticks_ms(), self.period))
        else:
            self.enabled = False

# 获取可以开始运行的任务
def get_due_task():
    t = _task_queue.peek()
    if t != None and ticks_diff(ticks_ms(), t.ph_key) >= 0:
        _task_queue.pop()
        return t.coro
    else:
        return None