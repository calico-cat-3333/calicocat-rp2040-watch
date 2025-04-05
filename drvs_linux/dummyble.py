import micropython
import time
import json
import os

from . import Device
from cces.log import log, ERROR, DEBUG

# 假装这里有蓝牙
_rpath = 'ble.txt'

class BLE(Device):
    def __init__(self):
        #self.uart = open(_rpath, 'rw')
        self.rx_line_buf = []
        self.rx_buf = ''

        self.sleeping = None
        self.dummy_state = False

    def at_reset(self):
        pass

    def at_mode(self, v=None):
        pass

    def connected(self):
        return self.dummy_state

    def sleep(self, mode=None):
        if mode == None:
            return False

    def uart_rx_int_cb(self, _):
        micropython.schedule(self.uart_rx_read_to_buf_ref, 0)

    def _decode(self, buf):
        # 传入的数据有时包含 ISO-8859-1 编码的数据，此时常规的 decode 方法不能正常工作
        try:
            dr = buf.decode()
        except UnicodeError:
            log('faild in unicode decode, try fallback decoder')
            try:
                dr = ''.join(chr(i) for i in buf)
            except Exception as e:
                log('faild in fallback decoder', exc=e, level=ERROR)
                return None
        except Exception as e:
            log('error in decode:', e, exc=e, level=ERROR)
            return None
        return dr

    def _rx_buf_parse(self):
        if not self.rx_buf.endswith('\n'):
            return

        if self.uart_rx_any() > 10:
            log('too may rx message in rx_line_buf, something must go wrong', level=ERROR)
            self.rx_line_buf.clear()

        if self.rx_buf == '\r\n':
            # empty line
            pass

        elif self.rx_buf[:4] == 'STA:':
            # status report
            log('ble report status update:', self.rx_buf)
            self.status_update(self.rx_buf.rstrip())

        elif self.rx_buf[:3] == '+OK' or self.rx_buf[:4] == '+ERR':
            # at command respons
            log('at command respons received:', self.rx_buf.rstrip())

        else:
            # payload
            self.rx_line_buf.append(self.rx_buf.rstrip())
            log('uart rx receive line:', self.rx_buf)

        self.rx_buf = ''

    def uart_rx_read_to_buf(self, _):
        while self.uart.any():
            try:
                #r = self.uart.readline()
                log('uart rx receive:', r, level=DEBUG)
            except Exception as e:
                log('faild in uart read:', e, exc=e, level=ERROR)
                self.rx_buf = ''
                return

            dr = self._decode(r)
            if dr == None:
                self.rx_buf = ''
                return

            self.rx_buf = self.rx_buf + dr
            self._rx_buf_parse()

    def reset(self):
        # 重置，硬重置优先，不能用才用软重置
        self.at_reset()

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

    def dummy_gb_respons(self, a):
        if not self.connected():
            return
        t = a.get('t')
        if t == 'findPhone':
            os.system('notify-send -u low -t 2000 "findPhone ' + str(a.get('n')) + '"')
            log('dummyble gb respons: findPhone', a.get('n'), 'received')
        if t == 'music':
            os.system('notify-send -u low -t 1000 "music ' + a.get('n') + '"')
            log('dummyble gb respons: music', a.get('n'), 'received')
            self.rx_line_buf.append('\x10GB({"t":"musicinfo","artist":"\u6d1b\u5929\u4f9d","album":"\u7acb\u6625","track":"\u7acb\u6625","dur":131,"c":-1,"n":1})')
            if a.get('n') == 'pause':
                self.rx_line_buf.append('\x10GB({"t":"musicstate","state":"pause","position":60,"shuffle":-1,"repeat":-1})')
            elif a.get('n') == 'play':
                self.rx_line_buf.append('\x10GB({"t":"musicstate","state":"play","position":60,"shuffle":-1,"repeat":-1})')
        if t in ['info', 'warn', 'error']:
            log('dummyble gb respons: msg:', a.get('msg'), 'received')
            os.system('notify-send -u low -t 2000 "send ' + t + ' ' + a.get('msg') + '"')

    def dummyconnect(self, s):
        self.dummy_state = s
        if s:
            self.rx_line_buf.append('')
            self.rx_line_buf.append("\x10setTime(1742316416);E.setTimeZone(8.0);(s=>s&&(s.timezone=8.0,require('Storage').write('setting.json',s)))(require('Storage').readJSON('setting.json',1))")
