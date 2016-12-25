import RPi.GPIO as GPIO
import time
import logging


LAUNCH_WAIT_TIME = 3
RELAY_TEST_DELAY = 0.5

output_pins = {
        'launch_1': 8,
        'launch_2': 11,
        'launch_3': 7,
        'launch_4': 5,
        'launch_5': 12,
        'launch_6': 6,
        'launch_7': 13,
        'launch_8': 16,
        'launch_9': 19,
        'launch_10': 20,
        'launch_11': 26,
        'launch_12': 21,
        'move_output_up': 25,
        'move_output_down': 9,
        'move_output_ccw': 10,
        'move_output_cw': 24}

input_pins = {
        'move_input_hor_1': 23,
        'move_input_hor_2': 22,
        'move_input_hor_3': 27,
        'move_input_ver_1': 17,
        'move_input_ver_2': 18,
        'move_input_ver_3': 15}


def gpio_init():
    GPIO.setmode(GPIO.BCM)

    for v in output_pins.values():
        GPIO.setup(v, GPIO.OUT, initial=GPIO.LOW)

    for v in input_pins.values():
        GPIO.setup(v, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


########### GPIO ############

def set_pin_high(pin):
    GPIO.output(pin, GPIO.HIGH)
    logging.info('Pin ' + str(pin) + ' on HIGH!')


def set_pin_low(pin):
    GPIO.output(pin, GPIO.LOW)
    logging.info('Pin ' + str(pin) + ' on LOW!')


def launch(rocket_id):
    set_pin_high(output_pins['launch_' + str(rocket_id)])
    time.sleep(LAUNCH_WAIT_TIME)
    set_pin_low(output_pins['launch_' + str(rocket_id)])


def launch_all():
    for pin in output_pins.values():
        set_pin_high(pin)

    time.sleep(LAUNCH_WAIT_TIME)

    for pin in output_pins.values():
        set_pin_low(pin)

    logging.info('All rockets launched!')


def move_cw():
    set_pin_high(output_pins['move_output_cw'])


def move_ccw():
    set_pin_high(output_pins['move_output_ccw'])


def move_up():
    set_pin_high(output_pins['move_output_up'])


def move_down():
    set_pin_high(output_pins['move_output_down'])


def move_stop():
    set_pin_low(output_pins['move_output_cw'])
    set_pin_low(output_pins['move_output_ccw'])
    set_pin_low(output_pins['move_output_up'])
    set_pin_low(output_pins['move_output_down'])


def relay_test():
    for pin in output_pins:
        set_pin_high(output_pins[pin])
        time.sleep(RELAY_TEST_DELAY)
        set_pin_low(output_pins[pin])
