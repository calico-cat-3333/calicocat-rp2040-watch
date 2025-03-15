from .task_scheduler import Task
from machine import Timer
from micropython import const

import time
import lvgl as lv

period = const(40)

def start():
    global lv_eventloop
    global lv_timer
    lv_timer = Timer(-1)
    lv_timer.init(mode=Timer.PERIODIC, period=period, callback=lv_eventloop_timer)
    lv_eventloop = Task(lv_eventloop_task, period)
    lv_eventloop.start()
    return (lv_eventloop, lv_timer)

def lv_eventloop_task():
    if lv._nesting.value == 0:
        lv.task_handler()

def lv_eventloop_timer():
    lv.tick_inc(period)
