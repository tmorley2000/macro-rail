import hardware_setup
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


from gui.core.ugui import Screen, ssd

from gui.widgets import Label, Button, CloseButton
from gui.core.writer import Writer
import gui.fonts.arial10 as arial10
from gui.core.colors import *

class BaseScreen(Screen):

    def __init__(self):

        def my_callback(button, arg):
            print('Button pressed', arg)
        def move_callback(button, arg):
            movemm(arg)

        super().__init__()
        wri = Writer(ssd, arial10, verbose=False)  # Monochrome display

        col = 2
        row = 2
        Label(wri, row, col, 'Simple Demo')
	Button(wri, 25, 2, text='in', callback=move_callback, args=(1,))
	Button(wri, 25, 62, text='out', callback=move_callback, args=(-1,))
        row = 50
        Button(wri, row, col, text='Yes', callback=my_callback, args=('Yes',))
        col += 60
        Button(wri, row, col, text='No', callback=my_callback, args=('No',))
        CloseButton(wri)  # Quit the application

def main():
	Screen.change(BaseScreen)
	

