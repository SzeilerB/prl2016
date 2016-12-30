import logging
import time
from gpio import GPIOHandler
from flask import Flask, jsonify, request
from threading import Thread
from ky040 import KY040Horizontal, KY040Vertical

MOVEMENT_TEST_DELAY = 1


class Tube:

    def __init__(self, _id):
        self.loaded = False
        self._id = _id

    def __str__(self):
        return str(self.loaded) + str(self._id)

    def serialize(self):
        return {
            'id': self._id,
            'loaded': self.loaded,
        }


class LaunchingSystem:

    def __init__(self):
        self.armed = False
        self.tubes = []

        for i in range(1, 13):
            self.tubes.append(Tube(i))

    def __str__(self):
        return str(self.armed)

    def serialize(self):
        return {
            'armed': self.armed,
            'tubes': [t.serialize() for t in self.tubes],
        }


class Movement:
    def __init__(self):
        self.moving_ccw = False
        self.moving_cw = False
        self.moving_up = False
        self.moving_down = False


prl = LaunchingSystem()
movement = Movement()
app = Flask(__name__)


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


@app.route('/launch/load', methods=['POST'])
def load_tubes():
    if not request.json:
        return "No JSON received.", 400

    for r in request.json:
        prl.tubes[r-1].loaded = True

    return "Tube(s) loaded", 200


@app.route('/launch/fire', methods=['POST'])
def fire():
    if not request.json:
        return "No JSON received.", 400
    elif not prl.armed:
        return "System is not armed!", 403
    else:
        for r in request.json:
            if prl.tubes[r-1].loaded:
                gpioHandler.launch(r)
                prl.tubes[r-1].loaded = False

    return "Given rockets launched", 200


@app.route('/launch/fire/all', methods=['POST'])
def fire_all():
    if not prl.armed:
        return "System is not armed!", 403
    else:
        gpioHandler.launch_all()

    return "All rockets launched!", 200


@app.route('/test', methods=['GET'])
def _relay_test():
    gpioHandler.relay_test()
    return "Test finished", 200


@app.route('/move/start', methods=['POST'])
def start_movement():
    if not request.json:
        return "No JSON received.", 400

    if len(request.json) < 1 or len(request.json) > 2:
        return "Bad request, invalid json", 400

    if 'cw' in request.json and 'ccw' in request.json:
        return "Bad request, opposite directions", 400

    if 'up' in request.json and 'down' in request.json:
        return "Bad request, opposite directions", 400

    if 'cw' in request.json:
        if movement.moving_ccw:
            gpioHandler.stop_ccw()
            movement.moving_ccw = False
        gpioHandler.move_cw()
        movement.moving_cw = True

    if 'ccw' in request.json:
        if movement.moving_cw:
            gpioHandler.stop_cw()
            movement.moving_cw = False
        gpioHandler.move_ccw()
        movement.moving_ccw = True

    if 'up' in request.json:
        if movement.moving_down:
            gpioHandler.stop_down()
            movement.moving_down = False
        gpioHandler.move_up()
        movement.moving_up = True

    if 'down' in request.json:
        if movement.moving_up:
            gpioHandler.stop_up()
            movement.moving_up = False
        gpioHandler.move_down()
        movement.moving_down = True

    return "Moving in given direction", 200


@app.route('/move/stop', methods=['POST'])
def stop_movement():
    if not request.json:
        return "No JSON received.", 400

    if len(request.json) < 1 or len(request.json) > 2:
        return "Bad request, invalid json", 400

    if 'cw' in request.json and 'ccw' in request.json:
        return "Bad request, opposite directions", 400

    if 'up' in request.json and 'down' in request.json:
        return "Bad request, opposite directions", 400

    if 'cw' in request.json:
        gpioHandler.stop_cw()
        movement.moving_cw = False

    if 'ccw' in request.json:
        gpioHandler.stop_ccw()
        movement.moving_ccw = False

    if 'up' in request.json:
        gpioHandler.stop_up()
        movement.moving_up = False

    if 'down' in request.json:
        gpioHandler.stop_down()
        movement.moving_down = False

    return "Moving in given direction", 200


@app.route('/move/emergency', methods=['GET'])
def emergency_stop():
    gpioHandler.emergency_stop()
    movement.moving_cw = False
    movement.moving_ccw = False
    movement.moving_down = False
    movement.moving_up = False

    return "Emergency eliminated", 200


@app.route('/move/test', methods=['POST'])
def test_movement():
    gpioHandler.move_up()
    time.sleep(MOVEMENT_TEST_DELAY)
    gpioHandler.stop_up()

    gpioHandler.move_down()
    time.sleep(MOVEMENT_TEST_DELAY)
    gpioHandler.stop_down()

    gpioHandler.move_ccw()
    time.sleep(MOVEMENT_TEST_DELAY)
    gpioHandler.stop_ccw()

    gpioHandler.move_cw()
    time.sleep(MOVEMENT_TEST_DELAY*2)
    gpioHandler.stop_cw()

    gpioHandler.move_ccw()
    time.sleep(MOVEMENT_TEST_DELAY)
    gpioHandler.stop_ccw()

    return "Movement test finished", 200

########### APP #############

if __name__ == '__main__':
    logging.basicConfig(filename='prl2016.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    gpioHandler = GPIOHandler()
    gpioHandler.gpio_init()

    print "egy"
    t1 = Thread(target=gpioHandler.check_limit_switches)
    t1.daemon = True

    print "ketto"
    t2 = Thread(target=gpioHandler.rotary_encoder_horizontal)
    t2.daemon = True

    print "harom"
    t3 = Thread(target=gpioHandler.rotary_encoder_vertical)
    t3.daemon = True

    t1.start()
    t2.start()
    t3.start()
    print "negy"

    app.run(debug=True, host='0.0.0.0', port=8000)
