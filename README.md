# spilite
A lite wrapper for spidev. 

## Overview

Spilite is a wrapper for [spidev](https://pypi.org/project/spidev/). It adds

* Entry and exit behaviour so that a SPI device can be treated as a file handle
* Additional types to support different software controlled chip select schemes
  * single pin (active high or low)
  * hardware address decoder (e.g. 74HC138)

For pin behaviour, [gpiozero](https://pypi.org/project/gpiozero/) types are used. This approach assumes that the hardware control of the chip select is *not* used (i.e. not using the hardware flow control with the micro's own SPI controller).

## Example

```python
from spidev import SpiDev
from spilite import SpiLite, ChipSelectPin
# setup chip select pin
cs_pin = ChipSelectPin(21)
cs_pin.unselect()
# setup the SPI bus device (speed and cpol)
spi = SpiLite(SpiDev(), cs=cs_pin, max_speed_hz=1000000, mode=0b11)
# ...
# send/receive two bytes
buffer = [0xff, 0xab]
with spi as bus:
  bus.xfer2(buffer)
```

