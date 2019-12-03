import utime
import usocket
import ubinascii

from network import LoRa
from micropython import const

DR = const(5)
DR_MIN = const(0)


def get_device_eui():
    lora = LoRa(mode=LoRa.LORAWAN)
    print(ubinascii.hexlify(lora.mac()).upper().decode("utf-8"))


def nvram_erase():
    lora = LoRa(mode=LoRa.LORAWAN)
    lora.nvram_erase()


class LoRaWANNode:
    def __init__(self, app_eui, app_key):
        """setup LoRaWAN for the European 868 MHz region with OTAA"""
        self.app_eui = ubinascii.unhexlify(app_eui)
        self.app_key = ubinascii.unhexlify(app_key)

        self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
        self.socket = None

        self.setup()

    @property
    def has_joined(self):
        return self.lora.has_joined()

    def setup(self):
        """Try to restore from nvram or join the network with OTAA"""
        self.lora.nvram_restore()

        if not self.has_joined:
            self.join()
        else:
            self.open_socket()

    def join(self, timeout=30):
        try:
            timeout = timeout * 1000
            self.lora.join(
                activation=LoRa.OTAA,
                auth=(self.app_eui, self.app_key),
                timeout=timeout,
                dr=DR,
            )

            if self.has_joined:
                self.lora.nvram_save()
                self.open_socket()
        except TimeoutError:
            pass

    def open_socket(self, timeout=6):
        self.socket = usocket.socket(usocket.AF_LORA, usocket.SOCK_RAW)
        self.socket.setsockopt(usocket.SOL_LORA, usocket.SO_DR, DR)
        self.socket.settimeout(timeout)

    def reset(self):
        self.socket.close()
        self.lora.nvram_erase()
        self.join()

    def send(self, data):
        """Send out data as bytes"""
        if self.has_joined:
            if isinstance(data, (float, str, int)):
                data = bytes([data])
            self.socket.send(data)
            utime.sleep(2)
            self.lora.nvram_save()
