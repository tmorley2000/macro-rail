mpremote fs cp macrorail.py main.py :
mpremote fs mkdir :lib
mpremote fs cp -r lib/micropython-stepper/src/stepper :lib/

mpremote cp -r lib/SH1106 :lib/

mpremote fs mkdir :lib/umenu
mpremote fs cp -r lib/umenu/src/* :lib/umenu


mpremote reset
#mpremote soft-reset
