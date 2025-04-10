import time

from .task_scheduler import Task

from _asyncio import TaskQueue
from _asyncio import Task as _Task
from .log import log

from . import hal
from .activity import refresh_activity_on, REFRESHON

# 每日定时任务
# 位于后台的系统服务之一，同时提供部分计划任务相关的 API

daily_tasks = TaskQueue()
daily_tasks_list = []
daily_scheduler_task = None

class DailyTask:
    def __init__(self, func, starttime, weekdays=0b1111111, tag=None, enabled=True):
        # weekdays : example only on monday: 0b0000001, if zero set oneshot
        # tag: string, default None
        # func 最好是全局的函数，不要是类函数
        self.func = func
        self.task = _Task(self.run)
        self.starttime = starttime # (hour, min)
        self.weekdays = weekdays
        self.tag = tag
        daily_tasks_list.append(self)
        self.enabled = False
        if enabled:
            self.start()
        self.enabled = enabled # all daily task enable by default

    def start(self):
        if self.enabled:
            return
        self.enabled = True
        ct = time.localtime()
        self.targettime = time.mktime((ct[0], ct[1], ct[2], self.starttime[0], self.starttime[1], 0, 0, 0))
        if time.time() - self.targettime > 60: # 任务已超时
            self.targettime = self.targettime + 86400 # (24 * 60 * 60)
        daily_tasks.push(self.task, self.targettime)
        log('start dailytask', self.func.__name__, ', will run at', self.starttime, 'everyday')

    def stop(self):
        log('stop dailytask', self.func.__name__)
        self.enabled = False
        daily_tasks.remove(self.task)

    def set_starttime(self, starttime, weekdays):
        r = self.enabled
        if r:
            self.stop()
        self.starttime = starttime
        self.weekdays = weekdays
        if r:
            self.start()

    def remove(self):
        log('remove dailytask', self.func.__name__)
        self.stop()
        daily_tasks_list.remove(self)

    def run(self):
        log('dailytask', self.func.__name__, 'run start')
        wmask = 1 << time.localtime()[6]
        self.targettime = self.targettime + 86400 # (24 * 60 * 60)
        if self.weekdays == 0 or self.weekdays & wmask == wmask:
            self.func()
        if self.weekdays == 0:
            self.enabled = False
            return
        daily_tasks.push(self.task, self.targettime)

def check_loop():
    ct = time.time()
    while True:
        t = daily_tasks.peek()
        if t != None and t.ph_key < ct:
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

def sys_dailytask_zeroclock():
    hal.imu.clear_step()
    refresh_activity_on(REFRESHON.ZERO_CLOCK)

def reschedule_all():
    # call after set time
    log('reschedule all dailytask')
    for t in daily_tasks_list:
        t.stop()
        t.start()

def start():
    global daily_scheduler_task
    daily_scheduler_task = Task(check_loop, 10000)
    daily_scheduler_task.start()

    global dailytask_zeroclock
    sys_dailytask_zerooc = DailyTask(sys_dailytask_zeroclock, (0, 0), tag='sys')
