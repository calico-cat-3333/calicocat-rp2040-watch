from machine import UART
from pcf8574 import PCF8574
import micropython

from . import Device
from ..log import log, ERROR

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
        self.mod_pin = self.pcf8574.get_pin(2)
        self.rst_pin = self.pcf8574.get_pin(5)
        self.wkp_pin = self.pcf8574.get_pin(3)
        self.wkp_pin.value(0)

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
                if self.uart_rx_any() > 10:
                    log('too may rx message in rx_line_buf, something must go wrone', level=ERROR)
                    self.rx_line_buf.clear()
                self.rx_line_buf.append(self.rx_buf.rstrip())
                log('uart rx receive line:', self.rx_buf)
                self.rx_buf = ''

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
        if not tx_str.endswith('\r\n'):
            tx_str = tx_str + '\r\n'
        self.uart.write(tx_str)

    def uart_tx_raw(self, tx_raw):
        # 向蓝牙模块写入原始数据
        self.uart.write(tx_raw)

    def uart_rx_raw(self):
        # 从蓝牙模块读取原始数据，绝对用不到，因为有中断
        return self.uart.read()
