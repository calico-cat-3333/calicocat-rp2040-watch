from machine import Pin, SoftI2C, UART, PWM

btn = Pin(18)
scl = Pin(27)
sda = Pin(26)
buzzer_pin = Pin(28)
rx = Pin(17)
tx = Pin(16)

# uart0 = UART(0, baudrate=115200, rx=rx, tx=tx)
# buzzer = PWM(buzzer_pin)
si2c = SoftI2C(sda=sda, scl=scl, freq=400000)