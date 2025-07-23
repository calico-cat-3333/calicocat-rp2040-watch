# `daily_scheduler` 每日任务

在每天的固定时间执行任务。

## DailyTask(self, func, starttime, weekdays=0b1111111, tag=None, enabled=True) 类

每日任务，通过实例化该类可以注册一个每日任务。

参数 func 是任务函数，最好不要是类函数（除非保证该实例不会被销毁）。

参数 starttime 是一个元组，第一个值为任务开始时间的小时，第二个值是分钟。

参数 weekdays 是一个二进制位掩码，表示任务在一周的哪些天有效。例如 0b0000001 表示仅周一。如果设置为 0 表示这是一次性任务。

参数 tag 是字符串或 None, 可以给任务添加标签。

参数 enabled 是任务启用状态，默认任务创建后即启用。

### start(self)

启用任务。

### stop(self)

禁用任务。

### set_starttime(self, starttime, weekdays)

设置 starttime 和 weekdays.

### remove(self)

禁用并删除任务。

### enabled

布尔类型，表示该任务是否启用。只读，应该使用 start 和 stop 函数启用和禁用任务，而不应该直接修改该变量。

### starttime

元组，第一个值为任务开始时间的小时，第二个值是分钟。只读，应该使用 set_starttime 函数修改这个变量，而不是直接修改该变量。

### weekdays

二进制位掩码，表示任务在一周的哪些天有效。例如 0b0000001 表示仅周一。如果设置为 0 表示这是一次性任务。只读，应该使用 set_starttime 函数修改这个变量，而不是直接修改该变量。

### tag

字符串或 None, 表示任务标签。

## list_by_tag(tag='')

通过 tag 筛选任务。

## get_list()

返回已注册任务列表。

## reschedule_all()

重新安排所有已注册任务，应该在修改时间后调用一次。