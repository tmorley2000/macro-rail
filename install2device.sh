mpremote fs cp macrorail.py main.py :
mpremote fs mkdir :lib
mpremote fs cp -r lib/micropython-stepper/src/stepper :lib/

mpremote fs cp -r lib/micropython-micro-gui/gui :lib/
mpremote fs cp hardware_setup.py :

mpremote fs mkdir :lib/drivers
mpremote fs cp -r lib/micropython-nano-gui/drivers/sh1106 :lib/drivers
mpremote fs cp lib/micropython-nano-gui/drivers/boolpalette.py :lib/drivers


mpremote soft-reset
