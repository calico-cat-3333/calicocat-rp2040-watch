from machine import Pin

class GPIOButton:
    def __init__(self, pin, irq_type):
        self.pin = pin
        self.pin.irq()

