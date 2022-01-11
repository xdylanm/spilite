import gpiozero

class ActiveHighPin(gpiozero.OutputDevice):
    def __init__(self, pin):
        super(ActiveHighPin, self).__init__(pin, active_high=True, initial_value=False)

class ActiveLowPin(gpiozero.OutputDevice):
    def __init__(self, pin):
        super(ActiveLowPin, self).__init__(pin, active_high=False, initial_value=False)

class ChipSelectPin(ActiveLowPin):
    """A single chip select pin from GPIO. The pin is active low and
    initialized to high (off)"""
    def __init__(self, pin):
        super(ChipSelectPin, self).__init__(pin)

    def select(self):
        self.on()

    def unselect(self):
        self.off()
