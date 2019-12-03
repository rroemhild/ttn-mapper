# Disable LTE on FiPy devices

from network import LTE

# disable lte
lte = LTE()
lte.deinit()
