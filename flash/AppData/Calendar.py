## calendar app

import M5
from M5 import *
from ClockData import Time
from SaveFileModule import FileManager
import GlobalVars
import Chart

class Calendar:
    def __init__(self):
        self.Calendar_Pages = {}
        self.CalendarPageNum = 0
        self.clock = Time()
        
        GlobalVars.currentPageModule = self
        
        self.page0()
    
    def __call__(self):
        self.clock = Time()
        self.CalendarPageNum = 0
        
        GlobalVars.currentPageModule = self
        
        self.page0()

    def page0(self):
        M5.Lcd.clear(0x000000)
        M5.Lcd.fillRect(0, 0, M5.Lcd.width(), 20, 0xFFFFFF)
        Widgets.Label(self.clock.getClock(), 0, 0, 1, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu18)
        
        Chart.draw(5, 7, 0, 80, 120, 140,
              None,
              None,
              None,
              [False, "M", "T", "W", "T", "F", "S", "S"],
        )