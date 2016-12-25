import RPi.GPIO as GPIO
import time
import logging


class GPIOHandler:

    def __init__(self):
        pass

    LAUNCH_WAIT_TIME = 3
    RELAY_TEST_DELAY = 0.2

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

    def gpio_init(self):
        GPIO.setmode(GPIO.BCM)

        for v in self.output_pins.values():
            GPIO.setup(v, GPIO.OUT, initial=GPIO.LOW)

        for v in self.input_pins.values():
            GPIO.setup(v, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def set_pin_high(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        logging.info('Pin ' + str(pin) + ' on HIGH!')

    def set_pin_low(self, pin):
        GPIO.output(pin, GPIO.LOW)
        logging.info('Pin ' + str(pin) + ' on LOW!')

    def launch(self, rocket_id):
        self.set_pin_high(self.output_pins['launch_' + str(rocket_id)])
        time.sleep(self.LAUNCH_WAIT_TIME)
        self.set_pin_low(self.output_pins['launch_' + str(rocket_id)])

    def launch_all(self):
        for pin in self.output_pins.values():
            self.set_pin_high(pin)

        time.sleep(self.LAUNCH_WAIT_TIME)

        for pin in self.output_pins.values():
            self.set_pin_low(pin)

        logging.info('All rockets launched!')

    def move_cw(self):
        self.set_pin_high(self.output_pins['move_output_cw'])

    def move_ccw(self):
        self.set_pin_high(self.output_pins['move_output_ccw'])

    def move_up(self):
        self.set_pin_high(self.output_pins['move_output_up'])

    def move_down(self):
        self.set_pin_high(self.output_pins['move_output_down'])

    def move_stop(self):
        self.set_pin_low(self.output_pins['move_output_cw'])
        self.set_pin_low(self.output_pins['move_output_ccw'])
        self.set_pin_low(self.output_pins['move_output_up'])
        self.set_pin_low(self.output_pins['move_output_down'])

    def relay_test(self):
        for pin in self.output_pins:
            self.set_pin_high(self.output_pins[pin])
            time.sleep(self.RELAY_TEST_DELAY)
            self.set_pin_low(self.output_pins[pin])
