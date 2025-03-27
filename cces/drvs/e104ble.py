from machine import UART
from pcf8574 import PCF8574
import micropython
import time

from . import Device
from ..log import log, ERROR, DEBUG

# E104-BT5005A 蓝牙串口模块驱动
# 此驱动被设计为只能被一个服务读写
# 虽然没有任何措施保证

class E104BLE(Device):
    def __init__(self, rx, tx, pcf8574_i2c):
        self.rx_pin = rx
        self.tx_pin = tx
        self.uart = UART(0, rx=rx, tx=tx, baudrate=115200)
        self.uart_rx_read_to_buf_ref = self.uart_rx_read_to_buf
        self.uart.irq(handler=self.uart_rx_int_cb, trigger=UART.IRQ_RXIDLE)
        self.rx_line_buf = []
        self.rx_buf = ''

        self.pcf8574 = PCF8574(pcf8574_i2c)
        self.link_pin = self.pcf8574.get_pin(1)
        self.mod_pin = self.pcf8574.get_pin(2)
        self.wkp_pin = self.pcf8574.get_pin(3)
        self.disc_pin = self.pcf8574.get_pin(4)
        self.rst_pin = self.pcf8574.get_pin(5)
        self.wkp_pin.value(0)

        self.at_recv_connected = None
        self.sleeping = None

    def reset(self):
        f = self.at_mode()
        if not f:
            self.at_mode(True)
            time.sleep_ms(300)
        self.uart_tx_raw('AT+RESET')
        self.at_recv_connected = None
        self.sleeping = False
        time.sleep_ms(300)
        if not f:
            self.at_mode(False)
            time.sleep_ms(300)
        self.uart_rx_buf_clear()

    def at_mode(self, v=None):
        if v == None:
            return not self.mod_pin.value()
        self.mod_pin.value(not v)

    def status_update(self, status):
        if status == 'STA:connected':
            self.at_recv_connected = True
            return
        if status == 'STA:disconnected':
            self.at_recv_connected = False
            return
        if status == 'STA:wakeup':
            self.sleeping = False
            return
        if status == 'STA:sleep':
            self.sleeping = True

    def connected(self):
        return not self.link_pin.value()

    def sleep(self, mode=None):
        if mode == None:
            return not self.wkp_pin.value()
        self.wkp_pin.value(mode)

    def disconnect(self):
        self.disc_pin.value(0)
        time.sleep_ms(40)
        self.disc_pin.value(1)

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
                r = self.uart.readline()
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
        if not self.connected():
            return False
        log('uart send string:', tx_str, level=DEBUG)
        if not tx_str.endswith('\r\n'):
            tx_str = tx_str + '\r\n'
        self.uart.write(tx_str)

    def uart_tx_raw(self, tx_raw):
        # 向蓝牙模块写入原始数据
        if not self.connected():
            return False
        self.uart.write(tx_raw)
