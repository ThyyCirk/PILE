import M5
from M5 import *
from ClockData import Time
from SaveFileModule import FileManager
from Keyboard import keyboard
import GlobalVars

class Fitness:
    def __init__(self):
        self.weight = int(FileManager.search('weight'))
        self.height = int(FileManager.search('height'))
        self.stepCount = int(FileManager.search('steps'))
        self.stepGoal = int(FileManager.search('stepGoal'))
        self.clock = Time()
        self.FitnessPage_Pages = {
            0: self.Page0, # Now correctly matches the method name
            1: self.Page1,
        }
        self.FitnessPage_Pages_Index = 0
        
        GlobalVars.currentPageModule = self
        
        self.Page0() # Updated to match uppercase 'P'
    
    def __call__(self):
        self.weight = int(FileManager.search('weight'))
        self.height = int(FileManager.search('height'))
        self.stepCount = int(FileManager.search('steps'))
        self.stepGoal = int(FileManager.search('stepGoal'))
        self.clock = Time()
        
        GlobalVars.lastPageModule = GlobalVars.currentPageModule
        GlobalVars.currentPageModule = self
        self.FitnessPage_Pages[self.FitnessPage_Pages_Index]()

    def Page0(self): # Updated to uppercase 'P' for consistency
        
        M5.Lcd.clear(0x000000)
        M5.Lcd.fillRect(0, 0, M5.Lcd.width(), 20, 0xFFFFFF)
        Widgets.Label(self.clock.getClock(), 0, 0, 1, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu18)
        
        cal_deficit = self.weight * self.stepCount * 0.0005
        
        def fitnessRingsAnimation(): 
            l_steps = 0
            last_state = -1

            while l_steps < self.stepCount:
                l_steps += 1
                percent = (l_steps / self.stepGoal) * 100

                # map percent → 1–9
                state = int(percent / 12.5) + 1

                # clamp to 1..9 (NO ifs)
                state = max(1, min(9, state))

                if state != last_state:
                    M5.Lcd.drawPng(
                        f"/flash/res/img/Bars_FitnessPage/Steps/{state}.png",
                        2,
                        30,
                        0, 0,
                        0, 0,
                        1, 1
                    )
                    Speaker.tone(1200 * state, 35)
                    last_state = state
                    
        # --- FIXED INDENTATION STARTING HERE ---
        GlobalVars.ALLOW_NEXT_PAGE = True 
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN = False 
        
        M5.Lcd.drawPng(
            "/flash/res/img/Pile/PileWorkout.png",
            27,
            50,
            0, 0,
            0, 0,
            0.6, 0.6
        )
        
        fitnessRingsAnimation() # Call the animation normally

        Widgets.Label(f"{self.stepCount}/{self.stepGoal}", 15, 160, 1, 0x15616d, 0x000000, Widgets.FONTS.DejaVu18)
        Widgets.Label("steps", 15, 180, 1, 0x15616d, 0x000000, Widgets.FONTS.DejaVu18)
        
        Widgets.Label(f"{cal_deficit}", 15, 205, 1, 0xff7d00, 0x000000, Widgets.FONTS.DejaVu18)
        Widgets.Label("calories burned", 15, 225, 0.7, 0xff7d00, 0x000000, Widgets.FONTS.DejaVu18)
            
    def Page1(self):
        
        M5.Lcd.clear(0x000000)
        M5.Lcd.fillRect(0, 0, M5.Lcd.width(), 20, 0xFFFFFF)
        Widgets.Label(self.clock.getClock(), 0, 0, 1, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu18)
        
        GlobalVars.ALLOW_NEXT_PAGE = False
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN = True
        
        M5.Lcd.drawPng(
                    "/flash/res/img/misc/Body.png",
                    0,
                    0,
                    0, 0,
                    0, 0,
                    1, 1
                )
        
        M5.Lcd.drawPng(
                    "/flash/res/img/misc/FitnessPageBtns1.png",
                    0,
                    205,
                    0, 0,
                    0, 0,
                    1, 1
                )
    
    def ButtonClick(self):
        
        self.FitnessPage_Pages_Index += 1
        
        # FIXED: Changed > to >= to prevent KeyError on index 2
        if self.FitnessPage_Pages_Index >= len(self.FitnessPage_Pages):
            self.FitnessPage_Pages_Index = 0
        
        self.FitnessPage_Pages[self.FitnessPage_Pages_Index]()
    
    def ButtonClick_RIGHTBTN(self):
        if(self.FitnessPage_Pages_Index == 1):
            keyboard(False, 3, "weight")