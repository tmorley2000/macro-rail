import micropython
import machine
import time
import gc
from stepper import Stepper
from SH1106.sh1106 import SH1106_I2C
from umenu import umenu

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
    if stepper.is_target_reached():
        # 200 steps per rev, 4 * microstepping, 4mm per rev
        steps=mm*(200*4/4)
        pos=stepper.get_pos()
        stepper.target(pos+steps)

def currentmm():
    pos=stepper.get_pos()
    return pos/(200*4/4)

def setmm(mm):
    steps=mm*(200*4/4)
    stepper.stop()
    stepper.overwrite_pos(steps)
    stepper.target(steps)
    stepper.track_target()

def showcurrentmm():
    return str(currentmm())

def steppertest():
    for a in range(50):
        movemm(1)
	time.sleep(1)
        movemm(-1)
	time.sleep(1)

menu=umenu.Menu(display,5,10)

mainmenu=umenu.MenuScreen('Macro Rail')
mainmenu=mainmenu.add(umenu.InfoItem('Status:', showcurrentmm))
mainmenu=mainmenu.add(umenu.CallbackItem('Move In:', (movemm,-1)))
mainmenu=mainmenu.add(umenu.CallbackItem('Move Out:', (movemm,1)))
mainmenu=mainmenu.add(umenu.CallbackItem('Reset Pos:', (setmm,0)))

menu.set_screen(mainmenu)

#menu.set_screen(umenu.MenuScreen('Main Menu')
#		.add(umenu.InfoItem('Status:', '1'))
#		.add(umenu.InfoItem('Status:', '2'))
#		.add(umenu.InfoItem('Status:', '3'))
#		.add(umenu.InfoItem('Status:', '4'))
#    .add(umenu.ValueItem('Speed', 10, 1, 100, 1, print))
#    .add(umenu.EnumItem("Mode", ['Option 1', 'Option 2'], print, 0))
#    .add(umenu.ConfirmItem("Print XXX", (print, 'XXX'), "Do you wanna do that?", ('yeah, sure!', 'nah, sorry!')))
#    .add(umenu.InfoItem("TXT no action!"))
#		)

menu.draw()

sw1=machine.Pin(pinsw1,machine.Pin.IN,machine.Pin.PULL_UP)
sw2=machine.Pin(pinsw2,machine.Pin.IN,machine.Pin.PULL_UP)
sw3=machine.Pin(pinsw3,machine.Pin.IN,machine.Pin.PULL_UP)
sw4=machine.Pin(pinsw4,machine.Pin.IN,machine.Pin.PULL_UP)

def menu_click(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        menu.click()

sw1.irq(menu_click, machine.Pin.IRQ_FALLING)

def menu_next(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        menu.move(1)

sw2.irq(menu_next, machine.Pin.IRQ_FALLING)

def menu_prev(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        menu.move(-1)

sw3.irq(menu_prev, machine.Pin.IRQ_FALLING)

def menu_reset(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        menu.reset()

sw4.irq(menu_reset, machine.Pin.IRQ_FALLING)


def main():
	menu.draw()
