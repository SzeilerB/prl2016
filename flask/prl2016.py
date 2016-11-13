from flask import Flask, jsonify, request, abort
import logging
import RPi.GPIO as GPIO
import time

############ INIT ###########

app = Flask(__name__)
logging.basicConfig(filename='prl2016.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
GPIO.setmode(GPIO.BCM)

LAUNCH_WAIT_TIME = 3

pins = {'launch_1': 8,
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
        'launch_12': 21}


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


for v in pins.values():
    GPIO.setup(v, GPIO.OUT)
    GPIO.output(v, GPIO.LOW)


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


########### GPIO ############

def set_pin_high(pin):
    GPIO.output(pin, GPIO.HIGH)
    logging.info('Pin ' + str(pin) + ' on HIGH!')


def set_pin_low(pin):
    GPIO.output(pin, GPIO.LOW)
    logging.info('Pin ' + str(pin) + ' on LOW!')


def launch(rocket_id):
    set_pin_high(pins['launch_' + str(rocket_id)])
    time.sleep(LAUNCH_WAIT_TIME)
    set_pin_low(pins['launch_' + str(rocket_id)])


def launch_all():
    for pin in pins.values():
        set_pin_high(pin)

    time.sleep(LAUNCH_WAIT_TIME)

    for pin in pins.values():
        set_pin_low(pin)

    logging.info('All rockets launched!')


########### APP #############

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
