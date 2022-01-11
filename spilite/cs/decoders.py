from .pins import ActiveHighPin

class AddressDecoder:
    """An addressable decoder (i.e. 74HC138). Adress lines are active high.
    The physical decoder is responsible for the active high or active low 
    behavior of the output lines"""
    def __init__(self, addr_pins, enable_pin=None):
        self.addr_pins = [ActiveHighPin(pin) for pin in addr_pins]
        self.enable_pin = enable_pin
    
    def select(self, addr):
        tmp_addr = int(addr)
        if tmp_addr < 0 or tmp_addr >= 2**len(self.addr_pins):
            raise ValueError("The address {} is out of range of the available address pins {}".format(my_addr, len(self.addr_pins)))
        for p in self.addr_pins:
            p.value = 1 if 0x01 & tmp_addr else 0
            tmp_addr >>= 1
        if self.enable_pin is not None:
            self.enable_pin.on()

    def unselect(self, addr):
        if self.enable_pin is not None:
            self.enable_pin.off()

class ChipSelectDecoder:
    """An addressable collection of chip selects using a decoder"""
    def __init__(self, addr, decoder):
        self.addr = int(addr)
        self.decoder = decoder

    def select(self):
        self.decoder.select(self.addr)

    def unselect(self):
        self.decoder.unselect(self.addr)

