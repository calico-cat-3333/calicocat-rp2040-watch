import heapq
from time import ticks_ms, ticks_add, ticks_diff

# 简单的任务调度器，受 kmk_firmware 项目中使用的任务调度器启发
# 使用小根堆实现
# 系统核心，任务调度有它负责
# lvgl 事件相关的调度由 lvgl 的 event_loop 调度器负责，那个调度器使用中断完成调度，与这里不冲突。

# 任务队列
_task_queue = []

# 任务
class Task:
    def __init__(self, func, period, oneshot = False):
        self.func = func # 要运行的函数
        self.enabled = False
        self.period = period # 运行间隔，毫秒
        self.oneshot = oneshot # 仅运行一次

    def start(self):
        self.enabled = True
        task_push(self, ticks_add(ticks_ms(), self.period))

    def stop(self):
        self.enabled = False

    def run(self):
        if self.enabled:
            self.func()
            if not self.oneshot:
                task_push(self, ticks_add(ticks_ms(), self.period))
            else:
                self.enabled = False

    def __gt__(self, other):
        return False # 对于具有相同目标时刻的任务，总是遵循先来后到原则

# 将任务加入任务队列
# target_tick 为预计任务开始的时刻（目标时刻）
# 不保证在目标时刻开始执行，仅保证在目标时刻到达之前不会开始执行
def task_push(task, target_tick):
    heapq.heappush(_task_queue, (target_tick, task))

# 获取可以开始运行的任务
def get_due_task():
    if len(_task_queue) == 0:
        return None
    if ticks_diff(ticks_ms(), _task_queue[0][0]) >= 0:
        return heapq.heappop(_task_queue)[1]