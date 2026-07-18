import M5
from M5 import *
from SaveFileModule import FileManager
from Keyboard import keyboard
import GlobalVars
import _thread
import ButtonModule
from PageCount import Draw as PC

class Fitness_page:
    lock = _thread.allocate_lock()
    
    def __init__(self):
        self.weight = int(FileManager.search('weight'))
        self.height = int(FileManager.search('height'))
        self.stepCount = int(FileManager.search('steps'))
        self.stepGoal = int(FileManager.search('stepGoal'))
        self.FitnessPage_Pages = {
            0: self.Page0, # Now correctly matches the method name
            1: self.Page1,
        }
        self.FitnessPage_Pages_Index = 0
        
        self.pg_count = PC()
        
        GlobalVars.currentPageModule = self
        
        self.page_btns = {
            0: {"ButtonClick": "ScrollDown"},
            1: {"ButtonClick": "ScrollDown", "ButtonClick_RIGHTBTN": "Circle"}
        }
        ButtonModule.setupPages(self.page_btns)
        self.pg_count.setup("Down", len(self.FitnessPage_Pages))
        
        self.Page0() # Updated to match uppercase 'P'
   
    def __call__(self):
        self.weight = int(FileManager.search('weight'))
        self.height = int(FileManager.search('height'))
        self.stepCount = int(FileManager.search('steps'))
        self.stepGoal = int(FileManager.search('stepGoal'))
        
        GlobalVars.lastPageModule = type(GlobalVars.currentPageModule) if GlobalVars.currentPageModule else None
        GlobalVars.currentPageModule = self
        
        self.pg_count.setup("Left", len(self.FitnessPage_Pages))
        self.FitnessPage_Pages[self.FitnessPage_Pages_Index]()

    def Page0(self): # Updated to uppercase 'P' for consistency
        
        cal_deficit = self.weight * self.stepCount * 0.0005
        GlobalVars.topBarVisible = True
                    
        # --- FIXED INDENTATION STARTING HERE ---
        GlobalVars.ALLOW_NEXT_PAGE = True 
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN = False
        
        M5.Lcd.clear(0x000000)
        
        M5.Lcd.drawPng(
            "/flash/res/img/Pile/PileWorkout.png",
            27,
            50,
            0, 0,
            0, 0,
            0.6, 0.6
        )
        
        self.animation_gen = self.fitnessRingsAnimation()

        Widgets.Label(f"{self.stepCount}/{self.stepGoal}", 15, 160, 1, 0x15616d, 0x000000, Widgets.FONTS.DejaVu18)
        Widgets.Label("steps", 15, 180, 1, 0x15616d, 0x000000, Widgets.FONTS.DejaVu18)
        
        Widgets.Label(f"{cal_deficit}", 15, 205, 1, 0xff7d00, 0x000000, Widgets.FONTS.DejaVu18)
        Widgets.Label("calories burned", 15, 225, 0.7, 0xff7d00, 0x000000, Widgets.FONTS.DejaVu18)
        
        self.pg_count.update()
        
    def fitnessRingsAnimation(self):
        target_state = max(1, min(9, int((self.stepCount / self.stepGoal) * 100 / 12.5) + 1))
        for state in range(1, target_state + 1):
            M5.Lcd.drawPng(f"/flash/res/img/Bars_FitnessPage/Steps/{state}.png", 2, 30, 0, 0, 0, 0, 1, 1)
            Speaker.tone(1200 * state, 35)
            yield
            
    def Page1(self):
        
        GlobalVars.ALLOW_NEXT_PAGE = False
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN = True
        GlobalVars.topBarVisible = False
        StopIteration(self.animation_gen)
        
        M5.Lcd.clear(0x000000)
        
        Widgets.Label(f"{self.weight}kgs", 1, 40, 1, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
        
        Widgets.Label(f"{self.height}cm", 1, 120, 1, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
        
        M5.Lcd.drawPng(
                    "/flash/res/img/misc/Body.png",
                    0,
                    0,
                    0, 0,
                    0, 0,
                    1, 1
                )
        
        '''M5.Lcd.drawPng(
                    "/flash/res/img/misc/FitnessPageBtns1.png",
                    0,
                    205,
                    0, 0,
                    0, 0,
                    1, 1
                )'''
        
        self.pg_count.update()
    
    def ButtonClick(self):
        
        self.FitnessPage_Pages_Index += 1
        
        # FIXED: Changed > to >= to prevent KeyError on index 2
        if self.FitnessPage_Pages_Index >= len(self.FitnessPage_Pages):
            self.FitnessPage_Pages_Index = 0
        
        GlobalVars.currentPageModule_Index=self.FitnessPage_Pages_Index

        self.FitnessPage_Pages[self.FitnessPage_Pages_Index]()
    
    def ButtonClick_RIGHTBTN(self):
        if(self.FitnessPage_Pages_Index == 1):
            keyboard(False, 3, "weight")
            
    def tick(self):
        if self.animation_gen:
            try:
                next(self.animation_gen)
            except StopIteration:
                self.animation_gen = None