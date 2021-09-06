import spidev
import gpiozero

class ActiveHighPin(gpiozero.OutputDevice):
    def __init__(self, pin):
        super(ActiveHighPin, self).__init__(pin, active_high=True, initial_value=False)

class ActiveLowPin(gpiozero.OutputDevice):
    def __init__(self, pin):
        super(ActiveLowPin, self).__init__(pin, active_high=False, initial_value=False)

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

class ChipSelectPin(ActiveLowPin):
    """A single chip select pin from GPIO. The pin is active low and
    initialized to high (off)"""
    def __init__(self, pin):
        super(ChipSelectPin, self).__init__(pin)

    def select(self):
        self.on()

    def unselect(self):
        self.off()

class ChipSelectDecoder:
    """An addressable collection of chip selects using a decoder"""
    def __init__(self, addr, decoder):
        self.addr = int(addr)
        self.decoder = decoder

    def select(self):
        self.decoder.select(self.addr)

    def unselect(self):
        self.decoder.unselect(self.addr)

class SpiLite:
    def __init__(
        self, 
        spi_device,
        bus_id=0,
        dev_id=0,
        cs=None, 
        bits_per_word=8,
        lsbfirst=False,
        max_speed_hz=100000,
        mode=0b00):
        
        self._device = spi_device
        self._bus_id = bus_id
        self._dev_id = dev_id
        self.bits_per_word = bits_per_word
        self.lsbfirst = lsbfirst
        self.max_speed_hz = max_speed_hz
        self.mode = mode

        self._cs = cs
        if self._cs is not None:
            self._cs.unselect()
        
    def __enter__(self):
        self._device.open(self._bus_id, self._dev_id)
        self._device.bits_per_word = self.bits_per_word
        self._device.lsbfirst = self.lsbfirst
        self._device.max_speed_hz = self.max_speed_hz
        self._device.mode = self.mode
        if self._cs is not None:
            self._device.no_cs = True
            self._cs.select()
    
        # configured and selected
        return self._device

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._cs is not None:
            self._cs.unselect()
        self._device.close()
        


