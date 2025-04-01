import time

from .task_scheduler import Task

from _asyncio import TaskQueue
from _asyncio import Task as _Task
from .log import log

# 每日定时任务
# 位于后台的系统服务之一，同时提供部分计划任务相关的 API

daily_tasks = TaskQueue()
daily_tasks_list = []
daily_scheduler_task = None

class DailyTask:
    def __init__(self, func, starttime, weekdays=0b1111111, tag=None, enabled=True, oneshot=False):
        # weekdays : only on monday: 0b0000001
        # tag: string, default None
        # func 最好是全局的函数，不要是类函数
        self.func = func
        self.task = _Task(self.run)
        self.starttime = starttime # (hour, min)
        self.weekdays = weekdays # run only in these weekdays
        self.enabled = enabled # all daily task enable by default
        self.oneshot = oneshot
        self.tag = tag
        daily_tasks_list.append(self)
        self.start()

    def start(self):
        time = time.localtime()
        self.targettime = time.mktime((time[0], time[1], time[2], self.starttime[0], self.starttime[1], 0, 0, 0))
        daily_tasks.push(self.task, self.targettime)
        log('daiyltask', self.func.__name__, 'start, will run at', self.starttime, 'everyday')

    def stop(self):
        log('dailytask', self.func.__name__, 'stop')
        self.enabled = False
        daily_tasks.remove(self.task)

    def remove(self):
        log('dailytask', self.func.__name__, 'remove from list')
        self.stop()
        daily_tasks_list.remove(self)

    def run(self):
        log('dailytask', self.func.__name__, 'run start')
        wmask = 1 << time.localtime()[6]
        self.targettime = self.targettime + (24 * 60 * 60)
        if self.weekdays & wmask == wmask:
            self.func()
        if self.oneshot:
            self.enabled = False
            return
        daily_tasks.push(self.task, self.targettime)

def check_loop():
    ct = time.time()
    while True:
        t = daily_tasks.peek()
        if t != None and t.ph_key > ct:
            daily_tasks.pop()
            t.coro()
        else:
            return

def list_by_tag(tag=''):
    for dtask in daily_tasks_list:
        if dtask.tag == tag:
            yield dtask

def get_list():
    return daily_tasks_list

def start():
    global daily_scheduler_task
    daily_scheduler_task = Task(check_loop, 10000)
    daily_scheduler_task.start()
