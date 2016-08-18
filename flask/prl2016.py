from flask import Flask, jsonify
import logging
from enum import Enum

app = Flask(__name__)
logging.basicConfig(filename='prl2016.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


############# REST #############

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


prl = LaunchingSystem()


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
    prl.armed = False
    return "System disarmed", 200


@app.route('/launch/status', methods=['GET'])
def status():
    return jsonify(prl.serialize()), 200


########### GPIO ############

class Pin(Enum):
    launch_1 = 8
    launch_2 = 11
    launch_3 = 7
    launch_4 = 5
    launch_5 = 12
    launch_6 = 6
    launch_7 = 13
    launch_8 = 16
    launch_9 = 19
    launch_10 = 20
    launch_11 = 26
    launch_12 = 21


########### APP #############

if __name__ == '__main__':
    app.run(debug=True, port=8000)
