from machine import Pin, SPI, I2C, ADC

lcd_spi = SPI(1, baudrate=60000000, sck=Pin(10), mosi=Pin(11))
lcd_dc = Pin(8, Pin.OUT)
lcd_cs = Pin(9, Pin.OUT)
lcd_rst = Pin(13, Pin.OUT)
lcd_bl = Pin(25, Pin.OUT)


i2c1 = I2C(1, scl=Pin(7), sda=Pin(6))
tp_int = Pin(21)
tp_rst = Pin(22, Pin.OUT, value=1)
imu_int1 = Pin(23)
imu_int2 = Pin(24)

bat_adc = ADC(Pin(29))
