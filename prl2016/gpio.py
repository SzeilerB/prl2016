import RPi.GPIO as GPIO
import time
import logging
from ky040 import KY040Vertical, KY040Horizontal


class GPIOHandler:

    def __init__(self):
        self.moving_up = False
        self.moving_down = False
        self.moving_ccw = False
        self.moving_cw = False

    LAUNCH_WAIT_TIME = 1.5
    RELAY_TEST_DELAY = 0.3
    SWITCH_CHECK_INTERVAL = 0.2

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
        'move_output_up': 14,
        'move_output_up2': 2,
        'move_output_down': 3,
        'move_output_down2': 4,
        'move_output_cw': 24,
        'move_output_cw2': 25,
        'move_output_ccw': 9,
        'move_output_ccw2': 10}

    input_pins = {
        'move_input_hor_rotary_clk': 23,
        'move_input_hor_rotary_data': 22,
        'move_input_ver_rotary_clk': 17,
        'move_input_ver_rotary_data': 18,
        'move_input_ver_switch_down': 15,
        'move_input_ver_switch_up': 26,
        'move_input_hor_switch_left': 27,
        'move_input_hor_switch_right': 21}

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
        if not self.moving_cw:
            self.set_pin_high(self.output_pins['move_output_cw'])
            self.set_pin_high(self.output_pins['move_output_cw2'])
            self.moving_cw = True

    def move_ccw(self):
        if not self.moving_ccw:
            self.set_pin_high(self.output_pins['move_output_ccw'])
            self.set_pin_high(self.output_pins['move_output_ccw2'])
            self.moving_ccw = True

    def move_up(self):
        if not self.moving_up:
            self.set_pin_high(self.output_pins['move_output_up'])
            self.set_pin_high(self.output_pins['move_output_up2'])
            self.moving_up = True

    def move_down(self):
        if not self.moving_down:
            self.set_pin_high(self.output_pins['move_output_down'])
            self.set_pin_high(self.output_pins['move_output_down2'])
            self.moving_down = True

    def stop_cw(self):
        self.set_pin_low(self.output_pins['move_output_cw'])
        self.set_pin_low(self.output_pins['move_output_cw2'])
        self.moving_cw = False

    def stop_ccw(self):
        self.set_pin_low(self.output_pins['move_output_ccw'])
        self.set_pin_low(self.output_pins['move_output_ccw2'])
        self.moving_ccw = False

    def stop_up(self):
        self.set_pin_low(self.output_pins['move_output_up'])
        self.set_pin_low(self.output_pins['move_output_up2'])
        self.moving_up = False

    def stop_down(self):
        self.set_pin_low(self.output_pins['move_output_down'])
        self.set_pin_low(self.output_pins['move_output_down2'])
        self.moving_down = False

    def get_input_sw_down(self):
        return GPIO.input(self.input_pins['move_input_ver_switch_down'])

    def get_input_sw_up(self):
        return GPIO.input(self.input_pins['move_input_ver_switch_up'])

    def get_input_sw_left(self):
        return GPIO.input(self.input_pins['move_input_ver_switch_left'])

    def get_input_sw_right(self):
        return GPIO.input(self.input_pins['move_input_ver_switch_right'])

    def emergency_stop(self):
        self.set_pin_low(self.output_pins['move_output_cw'])
        self.set_pin_low(self.output_pins['move_output_cw2'])
        self.set_pin_low(self.output_pins['move_output_ccw'])
        self.set_pin_low(self.output_pins['move_output_ccw2'])
        self.set_pin_low(self.output_pins['move_output_up'])
        self.set_pin_low(self.output_pins['move_output_up2'])
        self.set_pin_low(self.output_pins['move_output_down'])
        self.set_pin_low(self.output_pins['move_output_down2'])
        self.moving_cw = False
        self.moving_down = False
        self.moving_ccw = False
        self.moving_up = False

    def check_limit_switches(self):
        while True:
            if self.moving_up and self.get_input_sw_up() == 1:
                self.stop_up()

            if self.moving_down and self.get_input_sw_down() == 1:
                self.stop_down()

            if self.moving_ccw and self.get_input_sw_left() == 1:
                self.stop_ccw()

            if self.moving_cw and self.get_input_sw_right() == 1:
                self.stop_cw()

            time.sleep(0.1)

    def rotary_encoder_vertical(self):
        ky040 = KY040Vertical(self.input_pins['move_input_ver_rotary_clk'], self.input_pins['move_input_ver_rotary_data'])
        ky040.start()

        try:
            while True:
                time.sleep(0.1)
        finally:
            ky040.stop()
            GPIO.cleanup()

    def rotary_encoder_horizontal(self):
        ky040 = KY040Horizontal(self.input_pins['move_input_hor_rotary_clk'], self.input_pins['move_input_hor_rotary_data'])
        ky040.start()

        try:
            while True:
                time.sleep(0.1)
        finally:
            ky040.stop()
            GPIO.cleanup()

    def relay_test(self):
        for pin in self.output_pins:
            self.set_pin_high(self.output_pins[pin])
            time.sleep(self.RELAY_TEST_DELAY)
            self.set_pin_low(self.output_pins[pin])
            time.sleep(self.RELAY_TEST_DELAY)

    def gpio_cleanup(self):
        GPIO.cleanup()
