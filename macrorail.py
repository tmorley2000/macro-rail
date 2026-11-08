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
    print('Click')
    camring.value(1)
    time.sleep(0.1)
    camtip.value(1)
    time.sleep(0.1)
    camtip.value(0)
    camring.value(0)

stepper=Stepper(pinstepperstep,pinstepperdir,en_pin=pinsteppersleep,speed_sps=2000)
stepper.enable(True)

def waitmove():
    print('waiting',stepper.is_target_reached())
    while not stepper.is_target_reached():
        print("sleep")
        time.sleep(0.1)
        
def setmm(mm):
    steps=mm*(200*4/4)
    stepper.stop()
    stepper.overwrite_pos(steps)
    stepper.target(steps)
    stepper.track_target()

def currentmm():
    pos=stepper.get_pos()
    return pos/(200*4/4)

def movetomm(mm):
    if stepper.is_target_reached():
        # 200 steps per rev, 4 * microstepping, 4mm per rev
        steps=mm*(200*4/4)
	print('Moving To',mm)
        stepper.target(steps)
    	waitmove()

def movebymm(mm):
    if stepper.is_target_reached():
        movetomm(currentmm()+mm)

def showcurrentmm():
    return str(currentmm())

def steppertest():
    for a in range(50):
        movebymm(1)
	time.sleep(1)
        movebymm(-1)
	time.sleep(1)

config={}
config['step']=1.0
config['count']=20

def config_get(x):
	return config.get(x,None)

def config_set(x,y):
	config[x]=y

def runseq():
    movetomm(0)
    time.sleep(1)
    expose()
    for x in range(config['count']):
        movebymm(config['step'])
        time.sleep(2)
        expose()
    time.sleep(1)
    movetomm(0)

menu=umenu.Menu(display,5,10)

mainmenu=umenu.MenuScreen('Macro Rail')
mainmenu=mainmenu.add(umenu.InfoItem('Posn',showcurrentmm))
mainmenu=mainmenu.add(umenu.CallbackItem('Run', runseq))
mainmenu=mainmenu.add(umenu.CallbackItem('Move In', (movebymm,-1)))
mainmenu=mainmenu.add(umenu.CallbackItem('Move Out', (movebymm,1)))
mainmenu=mainmenu.add(umenu.CallbackItem('Reset Zero', (setmm,0)))
mainmenu=mainmenu.add(umenu.CallbackItem('Move To Zero', (movetomm,0)))
mainmenu=mainmenu.add(umenu.CallbackItem('Move To End', (movetomm,config.get('step')*config.get('count'))))

configmenu=umenu.SubMenuItem('Config')
configmenu=configmenu.add(umenu.ValueItem('Step',(config_get,'step'),0,10,0.1,(config_set,'step')))
configmenu=configmenu.add(umenu.ValueItem('Exp Count',(config_get,'count'),0,100,1,(config_set,'count')))

mainmenu=mainmenu.add(configmenu)

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

def menu_click(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        menu.click()

def menu_next(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        menu.move(1)


def menu_prev(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        menu.move(-1)


def menu_reset(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        menu.reset()

sw1=machine.Pin(pinsw1,machine.Pin.IN,machine.Pin.PULL_UP)
sw2=machine.Pin(pinsw2,machine.Pin.IN,machine.Pin.PULL_UP)
sw3=machine.Pin(pinsw3,machine.Pin.IN,machine.Pin.PULL_UP)
sw4=machine.Pin(pinsw4,machine.Pin.IN,machine.Pin.PULL_UP)

sws=[sw1,sw2,sw3,sw4]
swcalls=[menu_click, menu_next, menu_prev, menu_reset]

#sw1.irq(menu_click, machine.Pin.IRQ_FALLING)
#sw2.irq(menu_next, machine.Pin.IRQ_FALLING)
#sw3.irq(menu_prev, machine.Pin.IRQ_FALLING)
#sw4.irq(menu_reset, machine.Pin.IRQ_FALLING)


def main():
    menu.draw()

    swstate=[1 for x in sws]

    while True:
        now=[x.value() for x in sws]
	if now!=swstate:
            print('Was:',swstate,'Now:',now)
            for pin,old,new,call in zip(sws,swstate,now,swcalls):
                if new!=old and new==0:
                    call(pin)
            swstate=now

