import time
import lvgl as lv

from machine import Timer
from micropython import const

from .task_scheduler import Task

PERIOD = const(40)

def start():
    global lv_eventloop
    global lv_timer
    lv_timer = Timer(-1)
    lv_timer.init(mode=Timer.PERIODIC, period=PERIOD, callback=lv_eventloop_timer)
    lv_eventloop = Task(lv_eventloop_task, PERIOD)
    lv_eventloop.start()
    return (lv_eventloop, lv_timer)

def lv_eventloop_task():
    if lv._nesting.value == 0:
        lv.task_handler()

def lv_eventloop_timer(t):
    lv.tick_inc(PERIOD)
