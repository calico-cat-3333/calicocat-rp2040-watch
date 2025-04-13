import time
from micropython import const
import gc
import json

from .log import log
from . import hal, settingsdb, gadgetbridge
from .task_scheduler import Task, TASKEXIT
import struct

_RECORD_PERIOD_MINUTE = const(10) # 暂定每 10 分钟记录一次
MAX_RECORD = const(144 * 2)

# 简易步数记录，暂时不写存储功能了先，最多缓存两天，有蓝牙连接就直接发送
# 用来同步数据到手机，之后也可以在别的地方用

step_buf = []

_lstp = 0
def record_func():
    global _lstp
    stp = hal.imu.get_step()
    stpd = stp - _lstp
    _lstp = stp
    if buf_any() > MAX_RECORD:
        step_buf.pop(0)
        # 算的是 UTC 时间
    ts = int(time.time() - (settingsdb.get('timezone', 0) * 3600))
    mov = min(255, stpd // _RECORD_PERIOD_MINUTE) # 暂时不按照 Bangle.js 原始实现的运动强度，这里算的是平均步频
    record_push(stpd, mov, ts)
    gc.collect()

def clear_buf():
    step_buf.clear()
    _lstp = 0

def buf_any():
    return len(step_buf)

def record_push(step, mov, ts):
    # 如果蓝牙连接，直接发送到设备
    # 否则保存到缓冲区
    if hal.ble.connected():
        gadgetbridge.send_act(step, 0, mov, ts=ts)
    step_buf.append(struct.pack('>iHB', ts, step, mov))

def buf_pop():
    return struct.unpack('>iHB', step_buf.pop(0))

def get_buf():
    return step_buf

rtact_enable = [False, False] # step, hr
def set_rtact_report(json_cmd):
    # enable realtime act receive
    global rtact_enable
    global _lrtstp
    rtact_enable[0] = json_cmd.get('stp', False)
    rtact_enable[1] = json_cmd.get('hrm', False)
    period = json_cmd.get('int', 10) * 1000
    if rtact_enable[0] or rtact_enable[1]:
        realtime_act_task.set_period(period)
        realtime_act_task.start()
    else:
        _lrtstp = 0
        realtime_act_task.stop()
    return

def actfetch_handler(json_cmd):
    global actfetch_cnt
    global actfetch_starttime
    actfetch_cnt = 0
    actfetch_starttime = json_cmd.get('ts', 0) // 1000
    log('actfetch start')
    hal.ble.uart_tx('{"state": "start", "t": "actfetch"}')
    actfetch_task.start()

_lrtstp = 0
def send_rtact():
    global _lrtstp
    if rtact_enable[0] == False and rtact_enable[1] == False:
        _lrtstp = 0
        return TASKEXIT
    if not hal.ble.connected():
        _lrtstp = 0
        return TASKEXIT
    stpd = 0
    hrm = 0
    if rtact_enable[0]:
        stp = hal.imu.get_step()
        if _lrtstp > stp: # 处理每日零点计步器归零
            _lrtstp = 0
        stpd = stp - _lrtstp
        _lrtstp = stp
    if rtact_enable[1]:
        # not support now
        hrm = 0
    gadgetbridge.send_act(stpd, hrm, rt=True)

actfetch_cnt = 0
actfetch_starttime = 0
def actfetch_func():
    # 参考 https://github.com/espruino/BangleApps/blob/master/apps/android/lib.js#L209
    global actfetch_cnt
    if buf_any() == 0:
        log('atfetch done with send count', actfetch_cnt)
        hal.ble.uart_tx(json.dumps({'t':'actfetch', 'state':'end', 'count':actfetch_cnt}))
        actfetch_cnt = 0
        return TASKEXIT
    else:
        r = buf_pop()
        while buf_any() and r[0] < actfetch_starttime:
            r = buf_pop()
        if r[0] >= actfetch_starttime:
            gadgetbridge.send_act(r[1], 0, mov=r[2], ts=r[0])
            actfetch_cnt = actfetch_cnt + 1

def start():
    global record_task
    global realtime_act_task
    global actfetch_task

    record_task = Task(record_func, _RECORD_PERIOD_MINUTE * 60 * 1000)
    record_task.start()

    realtime_act_task = Task(send_rtact, 10000) # default 10 s

    # 极限情况下，一天的数据总计 144 条，全部传输完成耗时 144 * 100 / 1000 = 14.4 秒
    actfetch_task = Task(actfetch_func, 100)
    # 注册解析器
    gadgetbridge.HANDLER_DICT['actfetch'] = actfetch_handler
    gadgetbridge.HANDLER_DICT['act'] = set_rtact_report