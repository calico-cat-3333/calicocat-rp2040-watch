import json
import time

from . import settingsdb
from . import hal
from .task_scheduler import Task, TASKEXIT
from .log import log, ERROR
from . import notification

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

def set_time(cmd):
    # "\x10setTime(1742316416);E.setTimeZone(8.0);(s=>s&&(s.timezone=8.0,require('Storage').write('setting.json',s)))(require('Storage').readJSON('setting.json',1))"
    # 发送于 2025 03 19 00:46
    # setTime 后面是 UTC 的 unix 时间戳
    # E.setTimeZone 后面是时区
    cmds = cmd.split(';')
    utctime = int(cmds[0][9:-1])
    timezone = float(cmds[1][14:-1])
    hal.rtc.set_time_unix(int(utctime + (timezone * 3600)))
    log('set time to', time.localtime())
    settingsdb.put('timezone', timezone)
    settingsdb.save_settings()

def find_device(enable=False):
    if enable:
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
    notification.send(ntitle, ntext, nid)

def remove_notify(notify_id):
    notification.remove(notify_id)

def gb_cmd_parse():
    if not hal.ble.uart_rx_any():
        return
    cmd = hal.ble.uart_rx()
    if len(cmd) < 10:
        # 太短的绝对不对
        log('not vaild cmd:', cmd, level=ERROR)
        return

    if cmd[:9] == '\x10setTime(' and cmd.endswith(',1))'):
        # 对设置时间的指令特殊处理
        # 通常这个指令发生在连接建立时，所以这里也会写连接建立后执行的任务
        set_time(cmd)
        status_report_task.start()
        return

    if cmd[:4] == '\x10GB(' and cmd.endswith(')'):
        # 符合指令格式
        try:
            json_cmd = json.loads(cmd[4:-1])
        except Exception as e:
            log('faild to parse json string:', cmd[4:-1], exc=e, level=ERROR)
            return

        t = json_cmd.pop('t', None)

        if t == 'notify':
            send_notify(json_cmd)
            return

        if t == 'notify-':
            remove_notify(json_cmd['id'])
            return

        if t == 'alarm':
            # set_alarm(json_cmd)
            return

        if t == 'find':
            # n: bool
            find_device(json_cmd.get('n', False))
            return

        if t == 'weather':
            # temp,hi,lo,hum,rain,uv,code,txt,wind,wdir,loc
            # 温度，最高温，最低温，湿度，降雨率，紫外线指数，天气代码，天气文本，风速，风向，位置文本
            # 温度单位都是开尔文，湿度、降雨率是整形百分比，紫外线指数是数字
            # 风速浮点数单位 km/h 风向单位度，正南方为 0 顺时针方向
            global weather_data
            weather_data = json_cmd
            weather_data['time'] = time.time()
            return

        if t == 'musicinfo':
            # artist,album,track,dur,c,n
            # 作曲家，专辑名，轨道名，时长(秒)，专辑数，轨道数
            # 前三个都是字符串，后两个没看出有啥用，都是 -1 似乎是整形，时长为秒
            global music_info
            music_info = json_cmd
            music_info['time'] = time.time()
            return

        if t == 'musicstate':
            # state:"play/pause",position,shuffle,repeat
            # 状态，播放位置（秒），随机，重复（都是 -1）
            global music_state
            music_state = json_cmd
            music_state['time'] = time.time()
            return

    # 不符合指令格式
    log('invalid cmd:', cmd, level=ERROR)
    return

def send_msg(msg_type, text):
    if msg_type not in ['info', 'warn', 'error']:
        log('invalid msg type:', msg_type, level=ERROR)
        return
    hal.ble.uart_tx(json.dumps({'t':msg_type, 'msg':text}))

def send_status():
    if not hal.ble.connected():
        return TASKEXIT
    bat_stat = hal.battery.dump()
    hal.ble.uart_tx(json.dumps({'t':'status', 'bat':round(bat_stat[2], 2), 'volt':bat_stat[0], 'chg':int(bat_stat[3])}))

def start():
    global beep_repeat_task
    global cmd_parse_task
    global status_report_task

    hal.ble.reset()

    beep_repeat_task = Task(hal.buzzer.play, 1000)
    beep_repeat_task.set_args([4000,0,4000])

    cmd_parse_task = Task(gb_cmd_parse, 100)
    cmd_parse_task.start()

    status_report_task = Task(send_status, 30000)
