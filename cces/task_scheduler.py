from _uasyncio import TaskQueue
from _uasyncio import Task as _Task
from time import ticks_ms, ticks_add, ticks_diff
from micropython import const

from .log import log

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
        self.oneshot = oneshot # 仅在 period ms 后运行一次，否则立刻执行并按照 period ms 为周期运行
        self.args = ()
        self.kwargs = {}

    def start(self):
        if self.enabled:
            return
        log('start task', self.func.__name__)
        self.enabled = True
        _task_queue.push(self._task, ticks_add(ticks_ms(), self.period * self.oneshot))

    def set_args(*args, **kwargs):
        if self.enabled:
            return
        self.args = args
        self.kwargs = kwargs

    def start_with_arg(self, *args, **kwargs):
        if self.enabled:
            return
        self.args = args
        self.kwargs = kwargs
        self.start()

    def stop(self):
        self.enabled = False
        # _task_queue.remove(self._task)

    def run(self):
        if not self.enabled:
            return
        ts = ticks_ms()
        r = self.func(*self.args, **self.kwargs)
        te = ticks_ms()
        tu = ticks_diff(te, ts)
        log('function ' + self.func.__name__ + ' timeuse:', tu, end=' ')
        if (not self.oneshot) and r != TASKEXIT: # 如果 self.func 返回了 11 表示任务主动退出
            wait = self.period - tu if self.period > tu else 0
            log('wait', wait, 'ms then run again')
            _task_queue.push(self._task, ticks_add(ticks_ms(), wait))
            log('task pushed', self.func.__name__)
        else:
            log('then exited')
            self.enabled = False

# 获取可以开始运行的任务
def get_due_task():
    t = _task_queue.peek()
    if t != None and ticks_diff(ticks_ms(), t.ph_key) >= 0:
        _task_queue.pop()
        log('pop task', t.func.__name__)
        return t.coro
    else:
        return None