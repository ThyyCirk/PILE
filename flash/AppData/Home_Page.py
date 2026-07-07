## HomePage app class
import M5
from M5 import *
from SaveFileModule import FileManager
import GlobalVars

class Home_Page:
    def __init__(self):
        self.stepCount = int(FileManager.search('steps'))
        self.stepGoal = int(FileManager.search('stepGoal'))
        self.page0()
        
    def __call__(self):
        self.stepCount = int(FileManager.search('steps'))
        self.stepGoal = int(FileManager.search('stepGoal'))
        self.page0()

    def page0(self):
        GlobalVars.topBarVisible = True
        
        M5.Lcd.clear(0x000000)
        
        M5.Lcd.drawPng(
            "/flash/res/img/Pile/PileSittingIdle.png",
            M5.Lcd.width() // 2 - 30,
            M5.Lcd.height() // 2 - 20,
            0, 0,
            0, 0,
            0.7, 0.7
        )

        M5.Lcd.drawPng(
            f"/flash/res/img/Bars_HomePage/Bar{self.PercentageBar()}.png",
            0,
            190,
            0, 0,
            0, 0,
            0.7, 0.7
        )

        Widgets.Label(f"{self.stepCount}", 25, 220, 1.3, 0xFFFFFF, 0x000000)
        
    def PercentageBar(self):
        percent = (self.stepCount / self.stepGoal) * 100

        # map percent → 0,25,50,75,100
        step = int(percent / 25) * 25

        # clamp safely
        return max(0, min(100, step))

    def ButtonHold(self):
        self.stepCount = self.stepCount + 10
        FileManager.write('steps', f'{self.stepCount}')
        
        Widgets.Label(f"{self.stepCount}", 25, 220, 1.3, 0xFFFFFF, 0x000000)
        M5.Lcd.drawPng(
            f"/flash/res/img/Bars_HomePage/Bar{self.PercentageBar()}.png",
            0,
            190,
            0, 0,
            0, 0,
            0.7, 0.7
        )