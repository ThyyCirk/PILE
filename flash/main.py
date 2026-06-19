# main.py
import time
import M5
from M5 import *

Widgets.Label("starting...", 0, 0, 1, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu18)

time.sleep(1)

exec(open("/flash/apps/tamagochi.py").read())