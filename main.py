import pycom
import utime
import machine
import usocket
import ubinascii

from network import LoRa

import settings

# setup LoRaWAN for the European 868 MHz region with OTAA.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
app_eui = ubinascii.unhexlify(settings.NODE_APP_EUI.replace(' ', ''))
app_key = ubinascii.unhexlify(settings.NODE_APP_KEY.replace(' ', ''))

# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# set the 3 default channels to the same frequency (must be before
# sending the OTAA join request)
lora.add_channel(0, frequency=settings.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=settings.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=settings.LORA_FREQUENCY, dr_min=0, dr_max=5)

# only join the network if the device was resetted. I
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    # reset lora settings and counter from nvram. increase counter by 1. If
    # counter is bigger tha none byte, reset counter.
    print('woke up from deepsleep, restore from nvram.')
    count = pycom.nvs_get('count') + 1
    if count > 255:
        count = 1
    lora.nvram_restore()
else:
    # reset counter and erase lora nvram
    print('device resetted, join ttn network')
    count = 1
    lora.nvram_erase()

    # join the network using OTAA
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key),
              timeout=0, dr=settings.LORA_NODE_DR)

    # wait until the module has joined the network
    while not lora.has_joined():
        utime.sleep(2.5)
        print('not joined yet...')

    print('network joined!')

# setup socket with blocking
s = usocket.socket(usocket.AF_LORA, usocket.SOCK_RAW)
s.setsockopt(usocket.SOL_LORA, usocket.SO_DR, settings.LORA_NODE_DR)
s.setblocking(True)

# print counter as payload
print('send payload = {}'.format(count))
s.send(bytes([count]))
utime.sleep(2)

# store lora settings and the counter to nvram
print('write to nvram')
lora.nvram_save()
pycom.nvs_set('count', count)

# enter deepsleep
print('enter deepsleep for {} seconds'.format(settings.NODE_DEEPSLEEP))
machine.deepsleep(settings.NODE_DEEPSLEEP * 1000)
