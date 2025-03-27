import machine
import micropython

from pcf8574 import PCF8574
from extboard import si2c, rx, tx

import time


# 配置 UART0，波特率 115200，TX 在 GP0，RX 在 GP1
uart = machine.UART(0, baudrate=115200, tx=tx, rx=rx)
pcf = PCF8574(si2c)
mod_pin = pcf.get_pin(2)
link_pin = pcf.get_pin(1)
rst_pin = pcf.get_pin(5)
wkp_pin = pcf.get_pin(3)
wkp_pin.value(0)
disc_pin = pcf.get_pin(4)

def at_mode(v=None):
    if v == None:
        return not mod_pin.value()
    mod_pin.value(not v)

def at_test():
    uart.write('AT')

def at_reset():
    f = at_mode()
    if not f:
        at_mode(True)
        time.sleep_ms(300)
    uart.write('AT+RESET')
    time.sleep_ms(300)
    if not f:
        at_mode(False)
        time.sleep_ms(300)

def uarttx(b):
    uart.write(b)
    
def uartwrx():
    time.sleep(1)
    if uart.any():
        print(uart.read())

print('setup E104-BT5005A ble module for cces useage')

at_mode(True)
uartwrx()
at_test()
uartwrx()
uarttx('AT+LOGMSG=1')
uartwrx()
print('enable logmsg')
uarttx(b'at+uuidsvr128=n@\x00\x01\xb5\xa3\xf3\x93\xe0\xa9\xe5\x0e$\xdc\xca\x9e')
uartwrx()
uarttx('at+uuidchara1=3')
uartwrx()
uarttx('at+uuidchara2=2')
uartwrx()
print('set uuid to NUS')
at_reset()

