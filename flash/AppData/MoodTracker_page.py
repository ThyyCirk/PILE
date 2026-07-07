## Mood tracker app

import M5
from M5 import *
from ClockData import Time   # don't alias it to "time" — collides with the time module
from SaveFileModule import FileManager
import GlobalVars
import Chart

class MoodTrackerApp:
    def __init__(self):
        self.clock = Time()
        self.pages = {
            0: self.page0,
            1: self.pageSetMood,
            2: self.pageMonthFeeling,
        }
        self.MoodTracker_Num = 0
        self.MoodTracker_Pile = 0
        self.mood = {
            0: "Rad",
            1: "Good",
            2: "Mid",
            3: "Bad",
            4: "Awful"
        }
        
        GlobalVars.currentPageModule = self
        self.page0()
    
    def __call__(self):
        self.clock = Time()
        self.MoodTracker_Num = 0
        self.MoodTracker_Pile = 0
        
        GlobalVars.currentPageModule = self
        
        self.page0()
    
    def page0(self):
        M5.Lcd.clear(0x000000)
        M5.Lcd.fillRect(0, 0, M5.Lcd.width(), 20, 0xFFFFFF)
        Widgets.Label(self.clock.getClock(), 0, 0, 1, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu18)
        
        GlobalVars.ALLOW_SETTINGS_PAGE = True
        GlobalVars.ALLOW_NEXT_PAGE = True
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN = False 
        GlobalVars.OVERRIDE_SETTINGS_BTN = False  
        
        this_week=[]
        t = self.clock.getTime()
        x = 0
        valFrom = t[2] - 6 if t[2] - 6 > 0 else 1
        valTo = t[2] if valFrom > 1 else 1
        for i in range(valFrom, valTo + 1):
            key=f"{i}_{t[1]}_{t[0]}"
            value=FileManager.search(key, '/flash/libs/moodTracker.txt')
            if value != None:
                insertV = [key, value, x]
                this_week.append(insertV)
            x+=1
        values = [int(value) for key, value, _ in this_week]
        values.sort()  # ascending order → best to worst

        n = len(values)
        if n > 0:
            if n % 2 == 1:
                median_value = values[n // 2]
            else:
                median_value = (values[n // 2 - 1] + values[n // 2]) / 2
        
        median_mood = self.mood[int(round(median_value))] if n > 0 else "no entries"
        
        M5.Lcd.setTextSize(1.4)
        M5.Lcd.setTextColor(0xFFFFFF, 0X000000)
        M5.Lcd.setCursor(0, 120)
        M5.Lcd.print(f"This week, \nyou're feeling \n{median_mood}")
        
        Chart.draw(5, 7, 20, 30, 60, 110,
              [False, 0x66FF66, 0xCCFF33, 0xFFFF00, 0xFF9900, 0xFF1100],
              None,
              None,
              [True, f"{t[2]-6}", f"{t[2]-5}", f"{t[2]-4}", f"{t[2]-3}", f"{t[2]-2}", f"{t[2]-1}", "TD"],
              this_week
        )
        
        M5.Lcd.drawPng(
            "/flash/res/img/misc/MoodTracker1.png",
            0,
            205,
            0, 0,
            0, 0,
            1, 1
        )
        
    def pageSetMood(self, confirm=False):
        M5.Lcd.clear(0x000000)
        M5.Lcd.fillRect(0, 0, M5.Lcd.width(), 20, 0xFFFFFF)
        Widgets.Label(self.clock.getClock(), 0, 0, 1, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu18)
        
        GlobalVars.ALLOW_SETTINGS_PAGE = False
        GlobalVars.ALLOW_NEXT_PAGE = False
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN = True
        GlobalVars.OVERRIDE_SETTINGS_BTN = True
        
        t = self.clock.getTime()
        
        if confirm:
            FileManager.write(f"{t[2]}_{t[1]}_{t[0]}", f"{self.MoodTracker_Pile}", '/flash/libs/moodTracker.txt')
            self.MoodTracker_Num = 0
            GlobalVars.ALLOW_SETTINGS_PAGE = True
            GlobalVars.ALLOW_NEXT_PAGE = True
            GlobalVars.OVERRIDE_NEXT_PAGE_BTN = False 
            GlobalVars.OVERRIDE_SETTINGS_BTN = False  
            self.page0()
            return
        
        imgs = [
            "/flash/res/img/Pile/PileHappy.png",
            "/flash/res/img/Pile/PileSmile.png",
            "/flash/res/img/Pile/PileIndifferent.png",
            "/flash/res/img/Pile/PileAngry.png",
            "/flash/res/img/Pile/PileFurious.png",
            ]
        
        if self.MoodTracker_Pile > len(imgs)-1:
            self.MoodTracker_Pile = 0
        elif self.MoodTracker_Pile < 0:
            self.MoodTracker_Pile = len(imgs)-1
        
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1)
        M5.Lcd.setCursor(0, 190)
        M5.Lcd.print(f"Add mood for: \n{t[2]}_{t[1]}_{t[0]}")
        
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(2)
        M5.Lcd.setCursor(40, 215)
        M5.Lcd.print(f"{self.mood[self.MoodTracker_Pile]}")
        
        M5.Lcd.drawPng(
            f"{imgs[self.MoodTracker_Pile]}",
            0,
            30,
            0, 0,
            0, 0,
            1, 1
        )
        
        M5.Lcd.drawPng(
            "/flash/res/img/misc/ArrowsMoodTracker.png",
            0,
            -20,
            0, 0,
            0, 0,
            1, 1
        )
        
    def pageMonthFeeling(self):
        M5.Lcd.clear(0x000000)
        M5.Lcd.fillRect(0, 0, M5.Lcd.width(), 20, 0xFFFFFF)
        Widgets.Label(self.clock.getClock(), 0, 0, 1, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu18)
        
        GlobalVars.ALLOW_SETTINGS_PAGE = False
        GlobalVars.ALLOW_NEXT_PAGE = False
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN = True
        GlobalVars.OVERRIDE_SETTINGS_BTN = True
        
        t = self.clock.getTime()
        
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1.8)
        M5.Lcd.setCursor(0, 30)
        M5.Lcd.print(f"This month:\n{t[1]}.{t[0]}.")
        
        def is_leap(year):
            return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

        def days_in_month(year, month):
            if month in (1, 3, 5, 7, 8, 10, 12):
                return 31
            if month in (4, 6, 9, 11):
                return 30
            return 29 if is_leap(year) else 28
        
        def draw(x, y, r=8, color=0x555555, letter=None):
            M5.Lcd.fillEllipse(x, y, r, r, color)
            if letter:
                M5.Lcd.setTextSize(0.85)
                M5.Lcd.setTextColor(0xFFFFFF, 0X000000)
                M5.Lcd.setCursor(x - len(letter) * 2, y + r + 2)
                M5.Lcd.print(letter)   
        
        colval = [0x66FF66, 0xCCFF33, 0xFFFF00, 0xFF9900, 0xFF1100]
        x=10
        y=90
        rows=7
        w=135
        adder=28
        divX=w//rows
        pos=[]
        to=days_in_month(t[0], t[1]) + 1
        for i in range(1, to):
            key=f"{i}_{t[1]}_{t[0]}"
            value=FileManager.search(key, '/flash/libs/moodTracker.txt')
            
            keyprev=f"{i-1}_{t[1]}_{t[0]}"
            valueprev=FileManager.search(keyprev, '/flash/libs/moodTracker.txt')
            
            cval = colval[int(value)] if value != None else 0x555555
            draw(x, y, 8, cval, f"{i}.")
            
            pos.append((x, y))
            
            if valueprev != None and value != None and len(pos) >= 2:
                x1, y1 = pos[-2]
                x2, y2 = pos[-1]
                M5.Lcd.drawLine(x1, y1, x2, y2, 0xffffff)
            
            x+=divX
                
            if i % 7 == 0:
                x=10
                y+=adder
                
    def ButtonClick(self):
        self.MoodTracker_Num += 1
        
        # FIXED: Changed > to >= to prevent KeyError on index 2
        if self.MoodTracker_Num >= len(self.pages):
            self.MoodTracker_Num = 0
        
        self.pages[self.MoodTracker_Num]()
    
    def ButtonHold(self):
        if self.MoodTracker_Num == 1:
            self.pageSetMood(True)

    def ButtonClick_LEFTBTN(self):
        self.MoodTracker_Pile -= 1
        self.pageSetMood()
    
    def ButtonClick_RIGHTBTN(self):
        self.MoodTracker_Pile += 1
        self.pageSetMood()