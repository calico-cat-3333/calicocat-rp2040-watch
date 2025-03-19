from machine import UART
from pcf8574 import PCF8574
import micropython
import time

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
        self.link_pin = self.pcf8574.get_pin(1)
        self.mod_pin = self.pcf8574.get_pin(2)
        self.wkp_pin = self.pcf8574.get_pin(3)
        self.disc_pin = self.pcf8574.get_pin(4)
        self.rst_pin = self.pcf8574.get_pin(5)
        self.wkp_pin.value(0)

        self.connected = None
        self.sleeping = None

    def at_reset(self):
        f = self.at_mode()
        if not f:
            self.at_mode(True)
            time.sleep_ms(300)
        self.uart_tx_raw('AT+RESET')
        self.connected = False
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

    def uart_rx_read_to_buf(self, _):
        while self.uart.any():
            try:
                r = self.uart.readline()
                log('uart rx receive:', r)
                self.rx_buf = self.rx_buf + r.decode()
            except Exception as e:
                log('faild in uart read:', e, exc=e, level=ERROR)
                self.rx_buf = ''
                return
            if self.rx_buf.endswith('\n'):
                if self.uart_rx_any() > 10:
                    log('too may rx message in rx_line_buf, something must go wrong', level=ERROR)
                    self.rx_line_buf.clear()
                if self.rx_buf == '\r\n':
                    pass
                elif self.rx_buf[:4] == 'STA:':
                    log('ble report status update:', self.rx_buf)
                    self.status_update(self.rx_buf.rstrip())
                elif self.rx_buf[:3] == '+OK' or self.rx_buf[:4] == '+ERR':
                    log('at command respons received:', self.rx_buf.rstrip())
                else:
                    self.rx_line_buf.append(self.rx_buf.rstrip())
                    log('uart rx receive line:', self.rx_buf)
                self.rx_buf = ''

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
        if not tx_str.endswith('\r\n'):
            tx_str = tx_str + '\r\n'
        self.uart.write(tx_str)

    def uart_tx_raw(self, tx_raw):
        # 向蓝牙模块写入原始数据
        self.uart.write(tx_raw)

    def uart_rx_raw(self):
        # 从蓝牙模块读取原始数据，绝对用不到，因为有中断
        return self.uart.read()
