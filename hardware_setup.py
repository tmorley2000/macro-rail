import machine
import gc

from drivers.sh1106.sh1106 import SH1106_I2C as SSD

pindispsda=6
pindispscl=7

dispsda=machine.Pin(pindispsda)
dispscl=machine.Pin(pindispscl)

i2c=machine.I2C(1,sda=dispsda, scl=dispscl, freq=400000)

gc.collect()
ssd=SSD(128,64,i2c,None,0x3c,rotate=180)

from gui.core.ugui import Display
nxt = machine.Pin(29, machine.Pin.IN, machine.Pin.PULL_UP)  # Move to next control
sel = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_UP)  # Operate current control
prev = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)  # Move to previous control
display = Display(ssd, nxt, sel, prev)



