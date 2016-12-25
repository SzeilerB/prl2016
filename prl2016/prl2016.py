import logging
import time
from gpio import GPIOHandler
from flask import Flask, jsonify, request

MOVEMENT_TEST_DELAY = 2


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

prl = LaunchingSystem()
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


@app.route('/launch/fire', methods=['POST'])
def fire():
    if not request.json:
        return "No JSON received.", 400
    elif not prl.armed:
        return "System is not armed!", 403
    else:
        for r in request.json:
            gpioHandler.launch(r)

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
        gpioHandler.move_cw()

    if 'ccw' in request.json:
        gpioHandler.move_ccw()

    if 'up' in request.json:
        gpioHandler.move_up()

    if 'down' in request.json:
        gpioHandler.move_down()

    return "Moving in given direction", 200


@app.route('/move/stop', methods=['POST'])
def stop_movement():
    gpioHandler.move_stop()
    return "Movement stopped", 200


@app.route('/move/test', methods=['POST'])
def test_movement():
    gpioHandler.move_up()
    time.sleep(MOVEMENT_TEST_DELAY)
    gpioHandler.move_stop()

    gpioHandler.move_down()
    time.sleep(MOVEMENT_TEST_DELAY)
    gpioHandler.move_stop()

    gpioHandler.move_ccw()
    time.sleep(MOVEMENT_TEST_DELAY)
    gpioHandler.move_stop()

    gpioHandler.move_cw()
    time.sleep(MOVEMENT_TEST_DELAY*2)
    gpioHandler.move_stop()

    gpioHandler.move_ccw()
    time.sleep(MOVEMENT_TEST_DELAY)
    gpioHandler.move_stop()

    return "Movement test finished", 200


########### APP #############

if __name__ == '__main__':
    logging.basicConfig(filename='prl2016.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    gpioHandler = GPIOHandler()
    gpioHandler.gpio_init()
    app.run(debug=True, host='0.0.0.0', port=8000)
