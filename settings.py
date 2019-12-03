from machine import Pin
from micropython import const

# OTAA auth
NODE_APP_EUI = ""  # Application EUI
NODE_APP_KEY = ""  # Application Key

# Send a package every x seconds
LOOP_DELAY = const(15)

# Pin the button is connected to
PIN = Pin.exp_board.G5
