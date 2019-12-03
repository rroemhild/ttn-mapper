import node
import time
import pycom

from machine import Pin
from micropython import const
from settings import PIN, LOOP_DELAY, NODE_APP_EUI, NODE_APP_KEY


_button = "button"
_loop = "loop"


class Mapper:
    def __init__(self):
        self.ttn = node.LoRaWANNode(NODE_APP_EUI, NODE_APP_KEY)
        self.btn = Pin(PIN, mode=Pin.IN, pull=Pin.PULL_UP)
        pycom.heartbeat(False)

    def send(self, trigger):
        # set led on trigger
        if trigger == _button:
            pycom.rgbled(0xFF0000)
        elif trigger == _loop:
            pycom.rgbled(0xFF00)

        self.ttn.send(bytes([1]))
        pycom.rgbled(0xFF)

    def run_forever(self):
        pycom.rgbled(0xFF)
        delay = const(100)
        delaytime = time.time()
        btn = self.btn

        while True:
            if btn() == 1:
                self.send(_button)
                delaytime = time.time() + LOOP_DELAY

            if time.time() > delaytime:
                self.send(_loop)
                delaytime = time.time() + LOOP_DELAY

            time.sleep_ms(delay)


def main():
    mapper = Mapper()
    mapper.run_forever()


main()
