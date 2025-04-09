import json
import time

from . import settingsdb
from . import hal
from .task_scheduler import Task, TASKEXIT
from .log import log, ERROR
from . import notification#, steprecord
from .activity import refresh_activity_on, REFRESHON

'''
实现 Gadgetbridge/Bangle.js 通信协议
该协议极其简单，基本是使用蓝牙串口发送 json 格式的数据
参考：http://www.espruino.com/Gadgetbridge
参考：https://github.com/Freeyourgadget/Gadgetbridge/blob/master/app/src/main/java/nodomain/freeyourgadget/gadgetbridge/service/devices/banglejs/BangleJSDeviceSupport.java
参考：https://codeberg.org/Freeyourgadget/Gadgetbridge/src/branch/master/app/src/main/java/nodomain/freeyourgadget/gadgetbridge/service/devices/banglejs/BangleJSDeviceSupport.java
参考：https://github.com/wasp-os/wasp-os/blob/master/wasp/gadgetbridge.py
接收到的数据多数以 '\x10GB(' 开头，以 ')' 结尾，中间是 json 字符串，可以使用 json.loads 转换
比较特殊的一个是连接之后的设置时间的命令，发送的是 Bangls.js 的原生代码，这里需要特殊处理一下
不打算完全实现完成，只实现必要的协议，剩下的直接放弃
发送的数据则是 json.dumps 直接生成的字符串，发送时拼接上 '\r\n' 蓝牙驱动会完成这个
'''

weather_data = {}
music_info = {}
music_state = {}
rtact_enable = [False, False] # step, hr

# 内部处理函数，外部不得调用
def set_time(cmd):
    # "\x10setTime(1742316416);E.setTimeZone(8.0);(s=>s&&(s.timezone=8.0,require('Storage').write('setting.json',s)))(require('Storage').readJSON('setting.json',1))"
    # 发送于 2025 03 19 00:46
    # setTime 后面是 UTC 的 unix 时间戳
    # E.setTimeZone 后面是时区
    cmds = cmd.split(';', 2)
    utctime = int(cmds[0][9:-1])
    timezone = float(cmds[1][14:-1])
    hal.rtc.set_time_unix(int(utctime + (timezone * 3600)))
    log('set time to', time.localtime())
    settingsdb.put('timezone', timezone)
    settingsdb.save_settings()

def find_device(json_cmd):
    if json_cmd.get('n', False):
        beep_repeat_task.start()
        return
    beep_repeat_task.stop()
    hal.buzzer.stop()

def send_notify(json_cmd):
    nid = json_cmd['id']
    ntitle = json_cmd['src']
    if json_cmd['title'] != '':
        ntitle = ntitle + ': ' + json_cmd['title']
    ntext = json_cmd['body']
    notification.send(ntitle, ntext, nid, popup=True)

def remove_notify(json_cmd):
    notification.remove(json_cmd['id'])

def update_weather_info(json_cmd):
    # temp,hi,lo,hum,rain,uv,code,txt,wind,wdir,loc
    # 温度，最高温，最低温，湿度，降雨率，紫外线指数，天气代码，天气文本，风速，风向，位置文本
    # 温度单位都是开尔文，湿度、降雨率是整形百分比，紫外线指数是数字
    # 风速浮点数单位 km/h 风向单位度，正南方为 0 顺时针方向
    global weather_data
    weather_data = json_cmd
    weather_data['time'] = time.time()
    refresh_activity_on(REFRESHON.GB_WEATHER)

def update_music_info(json_cmd):
    # artist,album,track,dur,c,n
    # 作曲家，专辑名，轨道名，时长(秒)，专辑数，轨道数
    # 前三个都是字符串，后两个没看出有啥用，都是 -1 似乎是整形，时长为秒
    global music_info
    music_info = json_cmd
    music_info['time'] = time.time()

def update_music_state(json_cmd):
    # state:"play/pause",position,shuffle,repeat
    # 状态，播放位置（秒），随机，重复（都是 -1）
    global music_state
    music_state = json_cmd
    music_state['time'] = time.time()
    refresh_activity_on(REFRESHON.GB_MUSIC)

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
    # global actfetch_cnt
    # global actfetch_starttime
    global _lstp
    actfetch_cnt = 0
    actfetch_starttime = json_cmd.get('ts', 0) // 1000
    log('actfetch start')
    hal.ble.uart_tx(json.dumps({'t':'actfetch', 'state':'start'}))
    hal.ble.uart_tx(json.dumps({'t':'act', 'stp':0, 'ts':(time.time() - 60) * 1000}))
    actfetch_task.start()

def dummy_handler(json_cmd):
    log('handler for', json_cmd, 'not supported yet.')

_HADNLER_DICT = {
    'notify': send_notify,
    'notify-': remove_notify,
    'find': find_device,
    'weather': update_weather_info,
    'musicinfo': update_music_info,
    'musicstate': update_music_state,
    'is_gps_active': lambda _: hal.ble.uart_tx(json.dumps({'t':'gps_power', 'status':False})),
    'act': set_rtact_report,
    'actfetch': actfetch_handler,
    'alarm': dummy_handler,
    'call': dummy_handler,
    }

def gb_cmd_parse():
    if not hal.ble.uart_rx_any():
        return
    cmd = hal.ble.uart_rx()
    if len(cmd) < 10 or '\x10' not in cmd or ')' not in cmd:
        # 太短的绝对不对，没有 '\x10' 绝对不对，没有 ')' 绝对不对
        log('not vaild cmd:', cmd, level=ERROR)
        return
    # 排除干扰（不知道是不是反复焊接的关系，现在偶尔会出现收到奇怪的字符的情况）
    s = cmd.find('\x10')
    cmd = cmd[s:]

    if cmd.startswith('\x10setTime(') and cmd.endswith(',1))'):
        # 对设置时间的指令特殊处理
        # 通常这个指令发生在连接建立时，所以这里也会写连接建立后执行的任务
        set_time(cmd)
        status_report_task.start()
        return

    if not (cmd.startswith('\x10GB(') and cmd.endswith(')')):
        # 不符合指令格式
        log('invalid cmd:', cmd, level=ERROR)
        return

    try:
        json_cmd = json.loads(cmd[4:-1])
    except Exception as e:
        log('faild to parse json string:', cmd[4:-1], exc=e, level=ERROR)
        return

    t = json_cmd.pop('t', None)

    if t not in _HADNLER_DICT:
        log(t, 'is not supported')
        return

    _HADNLER_DICT[t](json_cmd)

## 暴露在外的 API
def send_msg(msg_type, text):
    # 发送信息，类型为 info/warn/error, text 为字符串
    hal.ble.uart_tx(json.dumps({'t':msg_type, 'msg':text}))

def music_ctrl(cmd):
    # 发送音乐控制命令 'play', 'pause', 'next', 'previous', 'volumeup', 'volumedown'
    hal.ble.uart_tx(json.dumps({'t':'music', 'n':cmd}))

def find_phone(s):
    # 发送查找手机指令
    hal.ble.uart_tx(json.dumps({'t':'findPhone', 'n':s}))

## 内部服务任务函数
def send_status():
    global _lstp
    refresh_activity_on(REFRESHON.BLE_CONNECTION)
    if not hal.ble.connected():
        music_info.clear()
        music_state.clear()
        return TASKEXIT
    bat_stat = hal.battery.dump()
    hal.ble.uart_tx(json.dumps({'t':'status', 'bat':round(bat_stat[2], 2), 'volt':bat_stat[0], 'chg':int(bat_stat[3])}))

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
    hal.ble.uart_tx(json.dumps({'t':'act', 'hrm':hrm, 'stp':stpd, 'rt':1}))

_lstp = 0
def actfetch_func():
    global _lstp
    stp = hal.imu.get_step()
    if _lstp > stp: #处理每日零点计步器归零
        _lstp = 0
    stpd = stp - _lstp
    _lstp = stp
    actfetch_cnt = 1
    if stpd != 0:
        hal.ble.uart_tx(json.dumps({'t':'act', 'stp':stpd}))
        actfetch_cnt = 2
    hal.ble.uart_tx(json.dumps({'t':'actfetch', 'state':'end', 'count':actfetch_cnt}))
    log('actfetch done with', actfetch_cnt, 'records transfered')

def start():
    global beep_repeat_task
    global cmd_parse_task
    global status_report_task
    global realtime_act_task
    global actfetch_task

    hal.ble.reset()

    beep_repeat_task = Task(hal.buzzer.play, 1000)
    beep_repeat_task.set_args([4000,0,4000])

    cmd_parse_task = Task(gb_cmd_parse, 100)
    cmd_parse_task.start()

    status_report_task = Task(send_status, 30000)
    realtime_act_task = Task(send_rtact, 10000) # default 10 s

    actfetch_task = Task(actfetch_func, 500, oneshot=True)
