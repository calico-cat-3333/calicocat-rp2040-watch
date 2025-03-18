from micropython import const

_PCF8574_ADDRESS = const(0x20)

class Pin:
    def __init__(self, pcf, n):
        self.pcf = pcf
        self.n = n

    def value(self, val=None):
        if val == None:
            return self.pcf.read_pin(self.n)
        else:
            self.pcf.set_pin(self.n, val)

    def toggle(self):
        self.pcf.toggle_pin(self.n)

class PCF8574:
    def __init__(self, i2c, address = _PCF8574_ADDRESS):
        self.i2c = i2c
        self.address = address
        self.sbuf = bytearray([0xff])

    def get_pin(self, n):
        return Pin(self, n)

    def read_pin(self, n):
        buf = self._read()
        return (buf[0] & (1 << n)) >> n

    def set_pin(self, n, val):
        # set to 0 for out low
        # set to 1 for input or out light high
        if val:
            self.sbuf[0] = self.sbuf[0] | (1 << n)
        else:
            self.sbuf[0] = self.sbuf[0] & (~(1 << n))
        self._write()

    def toggle_pin(self, n):
        self.sbuf[0] = self.sbuf[0] ^ (1 << n)
        self._write()

    def _write(self):
        self.i2c.writeto(self.address, self.sbuf)

    def _read(self):
        return self.i2c.readfrom(self.address, 1)
