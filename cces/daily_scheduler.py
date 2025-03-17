import time

from .task_scheduler import Task

# 每日定时任务
# 位于后台的系统服务之一，同时提供部分计划任务相关的 API

daily_tasks = []

class DailyTask:
    def __init__(self, func, starttime, weekdays=(1,2,3,4,5,6,7)):
        self.func = func
        self.starttime = starttime # (hour, min)
        self.lrd = (0,0,0) # last run date
        self.weekdays = weekdays # run only in these weekdays

    def reach(self):
        # 判断任务需要执行
        now = time.localtime()
        if (now[3], now[4]) != self.starttime:
            return False
        if not (now[6] in self.weekdays):
            return False
        if self.lrd == (now[0], now[1], now[2]):
            return False
        self.lrd = (now[0], now[1], now[2])
        return True

    def enable(self):
        daily_tasks.append(self)

    def disable(self):
        daily_tasks.remove(self)

    def enabled(self):
        return (self in daily_tasks)

    def run(self):
        self.func()

def check_loop():
    for task in daily_tasks:
        if task.reach():
            task.run()

def get_all():
    return daily_tasks

def start():
    daily_scheduler_task = Task(check_loop, 30000)
    daily_scheduler_task.start()
