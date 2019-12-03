=======================================
Simple LoPy/FiPy tracker for TTN Mapper
=======================================

This node sends one byte every 15 seconds (can be modified in settings.py) or on button press if a button is connected to pin the pin defined in settings.py (default G5 on expansion board).

1. Add your device **Application EUI** and **Application Key** to settings.py
2. Upload settings.py, node.py and main.py to your device
3. Optional: Upload boot.py if you want to disable LTE on FiPY
4. Register the node with the TTN Mapper on your mobile device
5. Start the tracker app and have a walk
6. Profit
