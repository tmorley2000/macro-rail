import machine
import time
from stepper import Stepper

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




