import RPi.GPIO as GPIO


class KY040Vertical:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1

    def __init__(self, clock_in, data_pin):

        self.clockPin = clock_in
        self.dataPin = data_pin

        self.vertical_turn = 0

    def start(self):
        GPIO.add_event_detect(self.clockPin, GPIO.FALLING, callback=self.clock_callback, bouncetime=30)

    def stop(self):
        GPIO.remove_event_detect(self.clockPin)

    def clock_callback(self, pin):
        if GPIO.input(self.clockPin) == 0:
            data = GPIO.input(self.dataPin)
            if data == 1:
                self.vertical_turn += 1
            else:
                self.vertical_turn -= 1


class KY040Horizontal:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1

    def __init__(self, clock_in, data_pin):

        self.clockPin = clock_in
        self.dataPin = data_pin

        self.horizontal_turn = 0

    def start(self):
        GPIO.add_event_detect(self.clockPin, GPIO.FALLING, callback=self.clock_callback, bouncetime=30)

    def stop(self):
        GPIO.remove_event_detect(self.clockPin)

    def clock_callback(self, pin):
        if GPIO.input(self.clockPin) == 0:
            data = GPIO.input(self.dataPin)
            if data == 1:
                self.horizontal_turn += 1
            else:
                self.horizontal_turn -= 1