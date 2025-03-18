from machine import UART
from pcf8574 import PCF8574
import micropython

from . import Device
from .. import log

class E104BLE(Device):
    def __init__(self, rx, tx, pcf8574_i2c):
        self.rx_pin = rx
        self.tx_pin = tx
        self.uart = UART(0, rx=rx, tx=tx, baudrate=115200)
        self.uart.irq(handler=self.uart_rx_int_cb, trigger=UART.IRQ_RXIDLE)
        self.rx_line_buf = []
        self.rx_buf = ''

        self.pcf8574 = PCF8574(pcf8574_i2c)
        self.mod_pin = self.pcf8574.get_pin(2)
        self.rst_pin = self.pcf8574.get_pin(5)
        self.wkp_pin = self.pcf8574.get_pin(3)
        self.wkp_pin.value(0)

        self uart_rx_read_to_buf_ref = self.uart_rx_read_to_buf

    def at_mode(v=None):
        if v:
            return not self.mod_pin.value()
        self.mod_pin.value(not v)

    def uart_rx_int_cb(self, _):
        micropython.schedule(self.uart_rx_read_to_buf_ref, 0)

    def uart_rx_read_to_buf(self, _):
        while self.uart.any():
            r = self.uart.readline()
            log('uart rx receive:', r)
            self.rx_buf = self.rx_buf + r.decode()
            if self.rx_buf.endswith('\n'):
                self.rx_line_buf.append(self.rx_buf.rstrip())
                log('uart rx receive line:', self.rx_buf)
                self.rx_buf = ''

    def uart_rx_any():
        # 返回 rx_line_buf 中剩余的行数
        return len(self.rx_line_buf)

    def uart_rx(self):
        # 从 rx_line_buf 中取一行
        if len(self.rx_line_buf) == 0:
            return ''
        return self.rx_line_buf.pop(0)

    def uart_tx(self, tx_str):
        # 发送一个字符串，自动添加 '\r\n' 结尾
        if not tx_str.endswith('\r\n'):
            tx_str = tx_str + '\r\n'
        self.uart.write(tx_str)

    def uart_tx_raw(self, tx_raw):
        self.uart.write(tx_raw)

    def uart_rx_raw(self):
        return self.uart.read()
