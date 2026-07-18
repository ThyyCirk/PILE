import M5
from M5 import *
from ClockData import Time   # don't alias it to "time" — collides with the time module
import GlobalVars


class TopBar:
    def __init__(self):
        self.clock = Time()
        self.clock_str = self.clock.getClock()
        self.show = GlobalVars.topBarVisible
        self.CurrentApp = GlobalVars.currentPageModule
        
        self.ToolBarTools = {
                "Clock": True
            }

    def draw(self):
        if not self.show:
            return
        M5.Lcd.fillRect(0, 0, M5.Lcd.width(), 20, 0xFFFFFF)
        M5.Lcd.setTextColor(0x000000, 0xFFFFFF)
        M5.Lcd.setTextSize(1.5)
        M5.Lcd.setCursor(0, 1)
        M5.Lcd.print(self.clock_str)

    def tick(self):
        current_app = GlobalVars.currentPageModule
        current_show = GlobalVars.topBarVisible

        app_changed = current_app != self.CurrentApp
        show_changed = current_show != self.show

        self.CurrentApp = current_app
        self.show = current_show

        if app_changed or show_changed:
            self.draw()
            return

        t = self.clock.getClock()
        if t != self.clock_str:
            self.clock_str = t
            self.draw()