from flask import Flask, jsonify, request
import logging
import RPi.GPIO as GPIO
import time

############ INIT ###########

app = Flask(__name__)
logging.basicConfig(filename='prl2016.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
GPIO.setmode(GPIO.BCM)

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
        'move_output_left': 10,
        'move_output_right': 24}

input_pins = {
        'move_input_hor_1': 23,
        'move_input_hor_2': 22,
        'move_input_hor_3': 27,
        'move_input_ver_1': 17,
        'move_input_ver_2': 18,
        'move_input_ver_3': 15}


class Tube:

    def __init__(self, _id):
        self.loaded = False
        self.id = _id

    def __str__(self):
        return str(self.loaded) + str(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'loaded': self.loaded,
        }


class LaunchingSystem:

    def __init__(self):
        self.armed = False
        self.tubes = []

        for i in range(20):
            self.tubes.append(Tube(i))

    def __str__(self):
        return str(self.armed)

    def serialize(self):
        return {
            'armed': self.armed,
            'tubes': [t.serialize() for t in self.tubes],
        }


for v in output_pins.values():
    GPIO.setup(v, GPIO.OUT, initial=GPIO.LOW)

for v in input_pins.values():
    GPIO.setup(v, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prl = LaunchingSystem()

############# REST #############


@app.route('/')
def index():
    logging.info('INDEX')
    return "PRL2016"


@app.route('/launch/arm', methods=['POST'])
def arm():
    logging.info('ARM')
    prl.armed = True
    return "System armed", 200


@app.route('/launch/disarm', methods=['POST'])
def disarm():
    logging.info('DISARM')
    prl.armed = False
    return "System disarmed", 200


@app.route('/launch/status', methods=['GET'])
def status():
    return jsonify(prl.serialize()), 200


@app.route('/launch/fire', methods=['POST'])
def fire():
    if not request.json:
        return "No JSON received.", 400
    elif not prl.armed:
        return "System is not armed!", 403
    else:
        for r in request.json["tubeIds"]:
            launch(r)

    return "Given rockets launched", 200


@app.route('/launch/fire/all', methods=['POST'])
def fire_all():
    if not prl.armed:
        return "System is not armed!", 403
    else:
        launch_all()

    return "All rockets launched!", 200


@app.route('/test', methods=['GET'])
def relay_test():
    for pin in output_pins:
        set_pin_high(pin)
        time.sleep(RELAY_TEST_DELAY)
        set_pin_low(pin)


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


########### APP #############

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
