from flask import Flask, jsonify

app = Flask(__name__)


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
    return "PRL2016"


@app.route('/launch/arm', methods=['POST'])
def arm():
    prl.armed = True
    return "System armed", 200


@app.route('/launch/disarm', methods=['POST'])
def disarm():
    prl.armed = False
    return "System disarmed", 200


@app.route('/launch/status', methods=['GET'])
def status():
    return jsonify(prl.serialize()), 200


if __name__ == '__main__':
    app.run(debug=True, port=8000)
