import M5, time
from M5 import *

def setup():
    M5.begin()
    Widgets.fillScreen(0xFFFFFF)
    Widgets.setRotation(0)
    M5.Lcd.clear(0x000000)
    
def biranje():
    return 0
    
def loop():
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        print(M5.Lcd.width(), M5.Lcd.height())
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        M5.Lcd.setTextSize(1)
        try:
            from utility import print_error_msg
            print_error_msg(e)
        except:
            print(e)