import micropython
import time
import json
import sys
import os

from . import Device
from cces.log import log, ERROR, DEBUG

# 假装这里有蓝牙

class BLE(Device):
    def __init__(self, default_connected = False):
        self.rx_line_buf = []
        self.rx_buf = ''

        self.sleeping = None
        self.dummyconnect(default_connected)

    def connected(self):
        return self.dummy_state

    def sleep(self, mode=None):
        if mode == None:
            return False

    def reset(self):
        log('dummyble: reset')

    def uart_rx_buf_clear(self):
        self.rx_buf = ''
        self.rx_line_buf.clear()

    def uart_rx_any(self):
        # 返回 rx_line_buf 中剩余的行数
        return len(self.rx_line_buf)

    def uart_rx(self):
        # 从 rx_line_buf 中取一行
        if len(self.rx_line_buf) == 0:
            return ''
        return self.rx_line_buf.pop(0)

    def uart_tx(self, tx_str):
        # 发送一个字符串，自动添加 '\r\n' 结尾
        log('uart send string:', tx_str)
        try:
            a = json.loads(tx_str)
        except:
            a = {'t':None}
            log('can not generate dummy gb respons')
        self.dummy_gb_respons(a)
        #if not tx_str.endswith('\r\n'):
            #tx_str = tx_str + '\r\n'
        #self.uart.write(tx_str)

    def uart_tx_raw(self, tx_raw):
        # 向蓝牙模块写入原始数据
        log('uart send raw data:', tx_raw)
        #self.uart.write(tx_raw)

# only on dummy driver

    def dummy_gb_respons(self, a):
        if not self.connected():
            return
        t = a.get('t')
        if t == 'findPhone':
            if hasattr(os, 'system'):
                os.system('notify-send -u low -t 2000 "findPhone ' + str(a.get('n')) + '"')
            log('dummyble gb respons: findPhone', a.get('n'), 'received')
        if t == 'music':
            if hasattr(os, 'system'):
                os.system('notify-send -u low -t 1000 "music ' + a.get('n') + '"')
            log('dummyble gb respons: music', a.get('n'), 'received')
            self.rx_line_buf.append('\x10GB({"t":"musicinfo","artist":"\u6d1b\u5929\u4f9d","album":"\u7acb\u6625","track":"\u7acb\u6625","dur":131,"c":-1,"n":1})')
            if a.get('n') == 'pause':
                self.rx_line_buf.append('\x10GB({"t":"musicstate","state":"pause","position":60,"shuffle":-1,"repeat":-1})')
            elif a.get('n') == 'play':
                self.rx_line_buf.append('\x10GB({"t":"musicstate","state":"play","position":60,"shuffle":-1,"repeat":-1})')
        if t in ['info', 'warn', 'error']:
            log('dummyble gb respons: msg:', a.get('msg'), 'received')
            if hasattr(os, 'system'):
                os.system('notify-send -u low -t 2000 "send ' + t + ' ' + a.get('msg') + '"')

    def dummyconnect(self, s):
        self.dummy_state = s
        if s:
            self.rx_line_buf.append('\x10GB({"t":"is_gps_active"})')
            self.rx_line_buf.append('\x10GB({"t":"is_gps_active"})')
            self.rx_line_buf.append("\x10setTime(1742316416);E.setTimeZone(8.0);(s=>s&&(s.timezone=8.0,require('Storage').write('setting.json',s)))(require('Storage').readJSON('setting.json',1))")
