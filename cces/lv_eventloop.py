from .task_scheduler import Task

import time
import lvgl as lv

def start():
    lv_eventloop = Task(lv_eventloop_task, 40)
    lv_eventloop.start()
    return lv_eventloop

last_tick = time.ticks_ms()

def lv_eventloop_task():
    global last_tick
    current_tick = time.ticks_ms()
    timeuse = time.ticks_diff(current_tick, last_tick)
    lv.tick_inc(timeuse)
    last_tick = current_tick
    if lv._nesting.value == 0:
        try:
            lv.task_handler()
        except Exception as e:
            print(e)
