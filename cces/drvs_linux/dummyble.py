import micropython
import time

from . import Device
from ..log import log, ERROR, DEBUG

# 假装这里有蓝牙
_rpath = 'ble.txt'

class BLE(Device):
    def __init__(self):
        #self.uart = open(_rpath, 'rw')
        self.rx_line_buf = []
        self.rx_buf = ''

        self.connected = None
        self.sleeping = None

    def at_reset(self):
        pass

    def at_mode(self, v=None):
        pass

    def status_update(self, status):
        if status == 'STA:connected':
            self.connected = True
            return
        if status == 'STA:disconnected':
            self.connected = False
            return
        if status == 'STA:wakeup':
            self.sleeping = False
            return
        if status == 'STA:sleep':
            self.sleeping = True

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
        if not tx_str.endswith('\r\n'):
            tx_str = tx_str + '\r\n'
        #self.uart.write(tx_str)

    def uart_tx_raw(self, tx_raw):
        # 向蓝牙模块写入原始数据
        log('uart send raw data:', tx_raw)
        #self.uart.write(tx_raw)

    def uart_rx_raw(self):
        # 从蓝牙模块读取原始数据，绝对用不到，因为有中断
        pass
