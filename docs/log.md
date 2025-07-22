# log 日志系统

一个简单的日志系统。

在 main.py 中使用 setlevel 调整日志等级，可以过滤日志输出。

日志等级：DEBUG INFO ERROR NOLOG

NOLOG 表示禁用日志输出。

## setlevel(level)

设置日志输出等级，不输出该级以下的日志。

参数 level 为枚举。

## log(*args, level=INFO, exc=None, **kwargs)

打印一条日志，用法跟 print 差不多。

特别的，参数 exc 可以在 try-catch 中使用，具有该参数后，将同时打印异常信息。

参数 level 表示这条日志的等级。

## get_time(f, *args, **kwargs)

装饰器，用于测量并在输出中打印某个函数的执行耗时。

