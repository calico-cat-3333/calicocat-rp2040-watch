import gc

from _asyncio import TaskQueue
from _asyncio import Task as _Task
from time import ticks_ms, ticks_add, ticks_diff, sleep_ms
from micropython import const

from .log import log, DEBUG

'''
简单的任务调度器，参考了 kmk_firmware 项目中使用的任务调度器
利用 _usyncio 中的 TaskQueue 配对堆实现
这些内容原本是为了 uasyncio 模块服务的，所以没有良好的文档记录
系统核心，任务调度有它负责
'''

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

    def set_args(self, *args, **kwargs):
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
        log('stop task', self.func.__name__)
        self.enabled = False
        _task_queue.remove(self._task)

    def run(self):
        if not self.enabled:
            return
        ts = ticks_ms()
        r = self.func(*self.args, **self.kwargs)
        te = ticks_ms()
        tu = ticks_diff(te, ts)
        if (not self.oneshot) and r != TASKEXIT: # 如果 self.func 返回了 11 表示任务主动退出
            wait = max(self.period - tu, 0)
            log('function', self.func.__name__, 'timeuse:', tu, 'wait', wait, 'ms then run again', level=DEBUG)
            _task_queue.push(self._task, ticks_add(ticks_ms(), wait))
        else:
            log('function', self.func.__name__, 'timeuse:', tu, 'then exit', level=DEBUG)
            self.enabled = False

def get_due_task():
    # 获取可以开始运行的任务
    t = _task_queue.peek()
    if t != None and ticks_diff(ticks_ms(), t.ph_key) >= 0:
        _task_queue.pop()
        return t.coro
    else:
        return None

_last_tick = 0
_free_time = 0
_buzy_time = 0
_sys_load = 0

def sys_load():
    global _free_time
    global _buzy_time
    global _last_tick
    global _sys_load
    ct = ticks_ms()
    timecost = ticks_diff(ct, _last_tick)
    _last_tick = ct
    _buzy_time = timecost - _free_time
    _sys_load = _buzy_time * 100 / timecost
    log('system load in last 10 secs:', _sys_load, '% buzy:', _buzy_time, 'ms free:', _free_time, 'ms')
    _free_time = 0
    gc.collect()

def get_sys_load_info():
    # 获取系统负载信息
    return (_sys_load, _buzy_time, gc.mem_free())

def start():
    # 启动调度器，并完全接管系统
    global sys_load_task
    global _free_time
    sys_load_task = Task(sys_load, 10000) # 每 10 秒计算一次系统负载
    sys_load_task.start()
    while True:
        task = get_due_task()
        if task != None:
            task()
        else:
            _free_time = _free_time + 1
            sleep_ms(1)
