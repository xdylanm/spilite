import spidev

class Port:
    def __init__(
        self, 
        max_speed_hz=100000,
        mode=0b00,
        cs=None, 
        bits_per_word=8,
        lsbfirst=False,
        bus_id=0,
        dev_id=0,
        spi_device=None):
        
        self._device = spi_device if spi_device is not None else spidev.SpiDev()
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

