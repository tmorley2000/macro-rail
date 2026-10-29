import machine
import time
import gc
from stepper import Stepper
from SH1106.sh1106 import SH1106_I2C

# Pin Numbers:
# 4 switches
pinsw1=29
pinsw2=28
pinsw3=27
pinsw4=26
# Display I2C
pindispsda=6
pindispscl=7
# Stepper driver
pinsteppersleep=2
pinstepperstep=3
pinstepperdir=4
# Camera remote
pincamtip=0
pincamring=1


pindispsda=6
pindispscl=7

dispsda=machine.Pin(pindispsda)
dispscl=machine.Pin(pindispscl)

i2c=machine.I2C(1,sda=dispsda, scl=dispscl, freq=400000)

gc.collect()
display=SH1106_I2C(128,64,i2c,None,0x3c,rotate=180)


# Camera Control
camtip=machine.Pin(pincamtip,machine.Pin.OUT)
camtip.value(0)
camring=machine.Pin(pincamring,machine.Pin.OUT)
camring.value(0)

def expose():
    camring.value(1)
    time.sleep(0.1)
    camtip.value(1)
    time.sleep(0.1)
    camtip.value(0)
    camring.value(0)

stepper=Stepper(pinstepperstep,pinstepperdir,en_pin=pinsteppersleep,speed_sps=2000)
stepper.enable(True)

def movemm(mm):
    # 200 steps per rev, 4 * microstepping, 4mm per rev
    steps=mm*(200*4/4)
    pos=stepper.get_pos()
    stepper.target(pos+steps)


def steppertest():
    for a in range(50):
        movemm(1)
	time.sleep(1)
        movemm(-1)
	time.sleep(1)


def main():
	from umenu import umenu
	menu=umenu.Menu(display,5,10)
	menu.set_screen(umenu.MenuScreen('Main Menu'))
	menu.draw()


	

