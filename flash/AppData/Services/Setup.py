import M5
from M5 import *
import time
from SaveFileModule import FileManager
import GlobalVars
from AppsModule import Apps

class Setup:
    def __init__(self):
        self.setupStage_Num = 0
        self.ageNum = time.localtime()[0] - 50
        self.height = 90
        self.weight = 40
        self.timezone = 0
        
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN = True
        GlobalVars.ALLOW_NEXT_PAGE = False
        GlobalVars.ALLOW_SETTINGS_PAGE = False
        
        self.stages = {
            0: self.stage0,
            1: self.stageTut,
            2: self.stage1,
            3: self.stage2,
            4: self.stage3,
            5: self.stage4,
            6: self.stage5,
            7: self.stageEND,
        }
        
        self.stages[self.setupStage_Num]()
        
    def stage0(self):
        
        M5.Lcd.clear(0x000000)
        Widgets.Label("Hello!", 0, 60, 1.3, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1.3)
        M5.Lcd.setCursor(0, 80)
        M5.Lcd.print("I'm your \ncompanion!")
        
        M5.Lcd.drawPng(
            "/flash/res/img/Pile/PileHappy.png",
            -10,
            130,
            0, 0,
            0, 0,
            1, 1
        )
        
        M5.Lcd.drawPng(
            "/flash/res/img/PageNext_Imgs/Next.png",
            0,
            205,
            0, 0,
            0, 0,
            1, 1
        )
        
    def stageTut(self):
        
        M5.Lcd.clear(0x000000)
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1.7)
        M5.Lcd.setCursor(0, 170)
        M5.Lcd.print("Hold or click \nto change \nvalues.")
        
        M5.Lcd.drawPng(
            "/flash/res/img/misc/RBtnThingy.png",
            0,
            0,
            0, 0,
            0, 0,
            1, 1
        )
        
        M5.Lcd.drawPng(
            "/flash/res/img/PageNext_Imgs/NextFinish.png",
            0,
            205,
            0, 0,
            0, 0,
            1, 1
        )
        
    def stage1(self):
        
        M5.Lcd.clear(0x000000)
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1.7)
        M5.Lcd.setCursor(0, 80)
        M5.Lcd.print("What's your \nage?")
        
        Widgets.Label(f"{self.ageNum}", 15, 140, 2, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
        
        M5.Lcd.drawPng(
            "/flash/res/img/PageNext_Imgs/Next.png",
            0,
            205,
            0, 0,
            0, 0,
            1, 1
        )
        
        if time.localtime()[0] - self.ageNum <= 0:
            self.ageNum = time.localtime()[0] - 100
            
    def stage2(self):
        maxHeight = 250
        minHeight = 90
        
        M5.Lcd.clear(0x000000)
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1.7)
        M5.Lcd.setCursor(0, 40)
        M5.Lcd.print("Hmm... \nHow tall \nare you?")
        
        Widgets.Label(f"{self.height} cm", 0, 140, 1, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
        
        M5.Lcd.drawPng(
            "/flash/res/img/PageNext_Imgs/Next.png",
            0,
            205,
            0, 0,
            0, 0,
            1, 1
        )
        
        M5.Lcd.drawPng(
            "/flash/res/img/Pile/StrechedOutPile.png",
            90,
            20,
            0, 0,
            0, 0,
            0.35, round((self.height / 200), 1)
        )
        
        if maxHeight - self.height  < 0:
            height = self.height
            
    def stage3(self):
        maxWeight = 200
        minWeight = 20
        
        M5.Lcd.clear(0x000000)
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1.7)
        M5.Lcd.setCursor(0, 90)
        M5.Lcd.print("What's your weight?")
        
        Widgets.Label(f"{self.weight} kg", 30, 145, 1.4, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
        
        M5.Lcd.drawPng(
            "/flash/res/img/PageNext_Imgs/Next.png",
            0,
            205,
            0, 0,
            0, 0,
            1, 1
        )
        
        M5.Lcd.drawPng(
            "/flash/res/img/Pile/StrechedOutPile.png",
            15,
            20,
            0, 0,
            0, 0,
            round((self.height / 150), 1), 0.5
        )
        
        if maxWeight - self.weight  < 0:
            self.weight = minWeight
    
    
    def stage4(self):
        M5.Lcd.clear(0x000000)
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1.2)
        M5.Lcd.setCursor(0, 25)
        M5.Lcd.print("What's your timezone?")
        
        if self.timezone > 12:
            self.timezone = -12
        
        Widgets.Label(f"{self.timezone} UTC", 30, 130, 1.3, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
        
        M5.Lcd.drawPng(
            "/flash/res/img/PageNext_Imgs/Next.png",
            0,
            205,
            0, 0,
            0, 0,
            1, 1
        )
        
    def stage5(self):
        M5.Lcd.clear(0x000000)
        Widgets.Label("LETS GO!", 0, 60, 1.3, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1.2)
        M5.Lcd.setCursor(0, 80)
        M5.Lcd.print("It's time to start your journey with PILE!")
        
        M5.Lcd.drawPng(
            "/flash/res/img/Pile/PileSmile.png",
            0,
            100,
            0, 0,
            0, 0,
            1, 1
        )
        
        M5.Lcd.drawPng(
            "/flash/res/img/PageNext_Imgs/NextFinish.png",
            0,
            205,
            0, 0,
            0, 0,
            1, 1
        )
        
    def stageEND(self):
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN = False 
        GlobalVars.ALLOW_NEXT_PAGE = True
        GlobalVars.ALLOW_SETTINGS_PAGE = True
        FileManager.write("WENT_THROUGH_SETUP", "True")
        
        FileManager.write("height", f"{self.height}")
        FileManager.write("weight", f"{self.weight}")
        FileManager.write("age", f"{self.ageNum}")
        FileManager.write("Timezone", f"{self.timezone}")
        #TIME = localtime_tz(timezone)
        
        Apps().get_page("HomePage")
        
    def ButtonClick(self):
        self.setupStage_Num += 1
        
        if self.setupStage_Num in self.stages:
            self.stages[self.setupStage_Num]()
        else:
            self.setupStage_Num = 0
            self.stages[self.setupStage_Num]()
        
    def ButtonClick_RIGHTBTN(self):
        if not GlobalVars.OVERRIDE_NEXT_PAGE_BTN or GlobalVars.ALLOW_NEXT_PAGE: return
        
        if self.setupStage_Num == 2:
            self.ageNum += 1
        elif self.setupStage_Num == 3:
            self.height += 1
        elif self.setupStage_Num == 4:
            self.weight += 1
        elif self.setupStage_Num == 5:
            self.timezone += 1
        else:
            return
        
        self.stages[self.setupStage_Num]()
        
    def ButtonHold_RIGHTBTN(self):
        if not GlobalVars.OVERRIDE_NEXT_PAGE_BTN or GlobalVars.ALLOW_NEXT_PAGE: return
        
        if self.setupStage_Num == 2:
            self.ageNum += 1
        elif self.setupStage_Num == 3:
            self.height += 1
        elif self.setupStage_Num == 4:
            self.weight += 1
        elif self.setupStage_Num == 5:
            self.timezone += 1
        else:
            return
        
        self.stages[self.setupStage_Num]()