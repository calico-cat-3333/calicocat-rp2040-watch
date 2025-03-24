import time
import sys
import lvgl as lv

from micropython import const

from .task_scheduler import Task

try:
    from machine import Timer
except:
    try:
        from lv_timer import Timer
    except:
        print('Timer not supported')

timer_id = 0
if sys.platform == 'rp2':
    timer_id = -1

PERIOD = const(20)

def start():
    global lv_eventloop
    global lv_timer
    lv_timer = Timer(timer_id)
    lv_timer.init(mode=Timer.PERIODIC, period=PERIOD, callback=lv_eventloop_timer)
    lv_eventloop = Task(lv_eventloop_task, PERIOD)
    lv_eventloop.start()
    return (lv_eventloop, lv_timer)

def lv_eventloop_task():
    if lv._nesting.value == 0:
        lv.task_handler()

def lv_eventloop_timer(t):
    lv.tick_inc(PERIOD)
