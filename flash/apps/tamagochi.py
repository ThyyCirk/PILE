import os, sys, io, time, ntptime, network, random, machine, math
import uasyncio as asyncio
import M5
from M5 import *

TIME = time.localtime() 

soundsStartPos = "/flash/res/audio/"
speaker = None

saveFile = "/flash/libs/data.txt"

Pages = ['HomePage', 'FitnessPage', 'MoodTrackerPage', 'FindMyPage']
currentPage = 0
currentPageFunc = ''
lastPage = ''

globalVolume = 100

## TIME SETUP
tm = time.localtime()
minutes = tm[3]
seconds = tm[4]

clock = f"{tm[3]:02d}:{tm[4]:02d}"

## LABELS
clocklabel = None
## TIME SETUP

stepGoal = 1000
stepCount = random.randint(1, stepGoal)
goalReached = False
weight = 70
height = 100
## labels

stepGoal_label = None

## SPECIAL BOOLEANS
ALLOW_NEXT_PAGE = True
ALLOW_SETTINGS_PAGE = True
OVERRIDE_NEXT_PAGE_BTN = False
OVERRIDE_SETTINGS_BTN = False
SOFTLOCK_PAGE = None

def setup():
    global speaker, weight, height, TIME
    M5.begin()
    Widgets.fillScreen(0xFFFFFF)
    Widgets.setRotation(0)
    M5.Lcd.clear(0x000000)
    
    '''if SearchSaveFile("Timezone") == "none" or SearchSaveFile("UTC") == "none":
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        wlan.active(True)
        wlan.connect(SearchSaveFile("WifiSSID"), SearchSaveFile("WifiPASS"))

        while not wlan.isconnected():
            pass
        
        try:
            ntptime.settime()
            utc_timestamp = time.time()
            WriteIntoSaveFile("UTC", int(utc_timestamp))
            print("UTC saved:", utc_timestamp)
        except OSError as e:
            print("NTP failed:", e)
        
        print("WiFi OK:", wlan.ifconfig())
  
    TIME = localtime_tz(int(SearchSaveFile("Timezone")))'''
    
    print(SearchSaveFile("WENT_THROUGH_SETUP"))
    if SearchSaveFile("WENT_THROUGH_SETUP") == "False":
        SetupPage()
    else:
        weight = int(SearchSaveFile("weight"))
        height = int(SearchSaveFile("height"))
        
        HomePage()
    
    globalStatus = int(SearchSaveFile('Audio', settings_saveFile))
    Speaker.setVolume(100 * globalStatus)
    Speaker.tone(7000, 50)
    time.sleep(0.1)
    Speaker.tone(9000, 50)
    time.sleep(0.1)
    Speaker.tone(10600, 100)
    
    speaker = M5.createSpeaker()
    speaker.begin()

def localtime_tz(offset_hours=0):
    saved_utc = SearchSaveFile("UTC")
    if saved_utc != "none":
        utc = int(saved_utc)
        return time.localtime(utc + offset_hours * 3600)
    else:
        return time.localtime(time.time() + offset_hours * 3600)

    
def HomePage():
    global clocklabel, stepGoal_label
    M5.Lcd.clear(0x000000)
    M5.Lcd.fillRect(0, 0, M5.Lcd.width(), 20, 0xFFFFFF)
    M5.Lcd.drawPng(
        "/flash/res/img/Pile/PileSittingIdle.png",
        M5.Lcd.width() // 2 - 30,
        M5.Lcd.height() // 2 - 20,
        0, 0,
        0, 0,
        0.7, 0.7
    )
    clocklabel = Widgets.Label(clock, 15, 50, 2, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    
    M5.Lcd.drawPng(
        f"/flash/res/img/Bars_HomePage/Bar{PercentageBar()}.png",
        0,
        190,
        0, 0,
        0, 0,
        0.7, 0.7
    )
    
    stepGoal_label = Widgets.Label(f"{stepCount}", 25, 220, 1.3, 0xFFFFFF, 0x000000)

FitnessPage_Pages_Index=0
def FitnessPage():
    global clock, clocklabel, stepGoal_label, weight, FitnessPage_Pages_Index
    
    M5.Lcd.clear(0x000000)
    M5.Lcd.fillRect(0, 0, M5.Lcd.width(), 20, 0xFFFFFF)
    clocklabel = Widgets.Label(clock, 0, 0, 1, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu18)
    
    cal_deficit = weight * stepCount * 0.0005
    
    def fitnessRingsAnimation(): 
        l_steps = 0
        last_state = -1

        while l_steps < stepCount:
            l_steps += 1
            percent = (l_steps / stepGoal) * 100

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
                
    def Page0():
        global ALLOW_NEXT_PAGE, OVERRIDE_NEXT_PAGE_BTN
        
        ALLOW_NEXT_PAGE=True  
        OVERRIDE_NEXT_PAGE_BTN=False 
        M5.Lcd.drawPng(
            "/flash/res/img/Pile/PileWorkout.png",
            27,
            50,
            0, 0,
            0, 0,
            0.6, 0.6
        )
        
        fitnessRingsAnimation()

        stepGoal_label = Widgets.Label(f"{stepCount}/{stepGoal}", 15, 160, 1, 0x15616d, 0x000000, Widgets.FONTS.DejaVu18)
        Widgets.Label(f"steps", 15, 180, 1, 0x15616d, 0x000000, Widgets.FONTS.DejaVu18)
        
        calc_label = Widgets.Label(f"{cal_deficit}", 15, 205, 1, 0xff7d00, 0x000000, Widgets.FONTS.DejaVu18)
        Widgets.Label(f"calories burned", 15, 225, 0.7, 0xff7d00, 0x000000, Widgets.FONTS.DejaVu18)
        
    def Page1():
        global ALLOW_NEXT_PAGE, OVERRIDE_NEXT_PAGE_BTN
        
        ALLOW_NEXT_PAGE=False
        OVERRIDE_NEXT_PAGE_BTN=True 
        M5.Lcd.drawPng(
                    f"/flash/res/img/misc/Body.png",
                    0,
                    0,
                    0, 0,
                    0, 0,
                    1, 1
                )
        
        M5.Lcd.drawPng(
                    f"/flash/res/img/misc/FitnessPageBtns1.png",
                    0,
                    205,
                    0, 0,
                    0, 0,
                    1, 1
                )
    
    FitnessPage_Pages={
        0: Page0,
        1: Page1
    }
    
    FitnessPage_Pages[FitnessPage_Pages_Index]()

def FitnessPage_ButtonClick():
    global FitnessPage_Pages_Index
    
    FitnessPage_Pages_Index+=1
    
    if FitnessPage_Pages_Index > 1:
        FitnessPage_Pages_Index = 0
    
    FitnessPage()
    
def FitnessPage_ButtonClick_RIGHTBTN():
    global FitnessPage_Pages_Index, weight
    if(FitnessPage_Pages_Index == 1):
        keyboard(False, 3, "weight")   

setupStage_Num = 0
ageNum = time.localtime()[0] - 100
timezone=0
def SetupPage():
    global setupStage_Num, currentPageFunc, OVERRIDE_NEXT_PAGE_BTN, ALLOW_NEXT_PAGE, ALLOW_SETTINGS_PAGE
    
    M5.Lcd.clear(0x000000)
    currentPageFunc = "SetupPage"
    OVERRIDE_NEXT_PAGE_BTN = True
    ALLOW_NEXT_PAGE = False
    ALLOW_SETTINGS_PAGE = False
    
    def stage0():
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
        
    def stageTut():
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
        
    def stage1():
        global ageNum
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1.7)
        M5.Lcd.setCursor(0, 80)
        M5.Lcd.print("What's your \nage?")
        
        Widgets.Label(f"{ageNum}", 15, 140, 2, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
        
        M5.Lcd.drawPng(
            "/flash/res/img/PageNext_Imgs/Next.png",
            0,
            205,
            0, 0,
            0, 0,
            1, 1
        )
        
        if time.localtime()[0] - ageNum <= 0:
            ageNum = time.localtime()[0] - 100
            
    def stage2():
        global height
        maxHeight = 250
        minHeight = 90
        
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1.7)
        M5.Lcd.setCursor(0, 40)
        M5.Lcd.print("Hmm... \nHow tall \nare you?")
        
        Widgets.Label(f"{height} cm", 0, 140, 1, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
        
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
            0.35, round((height / 200), 1)
        )
        
        if maxHeight - height  < 0:
            height = minHeight
            
    def stage3():
        global weight
        maxWeight = 200
        minWeight = 20
        
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1.7)
        M5.Lcd.setCursor(0, 90)
        M5.Lcd.print("Are you a \ntwunk or \na twink?")
        
        Widgets.Label(f"{weight} kg", 30, 145, 1.4, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
        
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
            round((height / 150), 1), 0.5
        )
        
        if maxWeight - weight  < 0:
            weight = minWeight
    
    
    def stage4():
        global timezone
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1.2)
        M5.Lcd.setCursor(0, 25)
        M5.Lcd.print("What's your timezone?")
        
        if timezone > 12:
            timezone = -12
        
        Widgets.Label(f"{timezone} UTC", 30, 130, 1.3, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
        
        M5.Lcd.drawPng(
            "/flash/res/img/PageNext_Imgs/Next.png",
            0,
            205,
            0, 0,
            0, 0,
            1, 1
        )
        
    def stage5():
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
        
    def stageEND():
        global OVERRIDE_NEXT_PAGE_BTN, ALLOW_NEXT_PAGE, ALLOW_SETTINGS_PAGE, ageNum, height, weight, timezone, TIME
        OVERRIDE_NEXT_PAGE_BTN = False 
        ALLOW_NEXT_PAGE = True
        ALLOW_SETTINGS_PAGE = True
        WriteIntoSaveFile("WENT_THROUGH_SETUP", "True")
        
        WriteIntoSaveFile("height", f"{height}")
        WriteIntoSaveFile("weight", f"{weight}")
        WriteIntoSaveFile("age", f"{ageNum}")
        WriteIntoSaveFile("Timezone", f"{timezone}")
        TIME = localtime_tz(timezone)
        
        HomePage()
    
    stages = {
        0: stage0,
        1: stageTut,
        2: stage1,
        3: stage2,
        4: stage3,
        5: stage4,
        6: stage5,
        7: stageEND,
    }
    
    if setupStage_Num in stages:
        stages[setupStage_Num]()
    else:
        setupStage_Num = 0
        stages[setupStage_Num]()
        
        
def SetupPage_ButtonClick():
    global setupStage_Num
    setupStage_Num += 1
    SetupPage()
    
def SetupPage_ButtonClick_RIGHTBTN():
    global OVERRIDE_NEXT_PAGE_BTN, ALLOW_NEXT_PAGE, setupStage_Num, ageNum, height, weight, timezone
    
    if not OVERRIDE_NEXT_PAGE_BTN or ALLOW_NEXT_PAGE: return
    
    if setupStage_Num == 2:
        ageNum += 1
    elif setupStage_Num == 3:
        height += 1
    elif setupStage_Num == 4:
        weight += 1
    elif setupStage_Num == 5:
        timezone += 1
    else:
        return
    
    SetupPage()
    
def SetupPage_ButtonHold_RIGHTBTN():
    global OVERRIDE_NEXT_PAGE_BTN, ALLOW_NEXT_PAGE, setupStage_Num, ageNum, height, weight, timezone
    
    if not OVERRIDE_NEXT_PAGE_BTN or ALLOW_NEXT_PAGE: return
    
    if setupStage_Num == 2:
        ageNum += 1
    elif setupStage_Num == 3:
        height += 1
    elif setupStage_Num == 4:
        weight += 1
    elif setupStage_Num == 5:
        timezone += 1
    else:
        return
    
    SetupPage()


MoodTracker_Num = 0
MoodTracker_Pile = 0
def MoodTrackerPage(confirm=False, specPage=False):
    global clock, clocklabel, MoodTracker_Num
    M5.Lcd.clear(0x000000)
    M5.Lcd.fillRect(0, 0, M5.Lcd.width(), 20, 0xFFFFFF)
    clocklabel = Widgets.Label(clock, 0, 0, 1, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu18)
    
    mood = {
        0: "Rad",
        1: "Good",
        2: "Mid",
        3: "Bad",
        4: "Awful"
    }
    
    ## MAIN PAGE
    def page0():
        global ALLOW_SETTINGS_PAGE, ALLOW_NEXT_PAGE, OVERRIDE_NEXT_PAGE_BTN, OVERRIDE_SETTINGS_BTN
        
        ALLOW_SETTINGS_PAGE = True
        ALLOW_NEXT_PAGE = True
        OVERRIDE_NEXT_PAGE_BTN = False 
        OVERRIDE_SETTINGS_BTN = False  
        
        this_week=[]
        t = time.localtime()
        x = 0
        valFrom = t[2] - 6 if t[2] - 6 > 0 else 1
        valTo = t[2] if valFrom > 1 else 1
        for i in range(valFrom, valTo + 1):
            key=f"{i}_{t[1]}_{t[0]}"
            value=SearchSaveFile(key, '/flash/libs/moodTracker.txt')
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
        
        median_mood = mood[int(round(median_value))] if n > 0 else "no entries"
        
        M5.Lcd.setTextSize(1.4)
        M5.Lcd.setTextColor(0xFFFFFF, 0X000000)
        M5.Lcd.setCursor(0, 120)
        M5.Lcd.print(f"This week, \nyou're feeling \n{median_mood}")
        
        Chart(5, 7, 20, 30, 60, 110,
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
        
    def pageSetMood():
        global MoodTracker_Pile, MoodTracker_Num, ALLOW_SETTINGS_PAGE, ALLOW_NEXT_PAGE, OVERRIDE_NEXT_PAGE_BTN, OVERRIDE_SETTINGS_BTN
        
        ALLOW_SETTINGS_PAGE = False
        ALLOW_NEXT_PAGE = False
        OVERRIDE_NEXT_PAGE_BTN = True
        OVERRIDE_SETTINGS_BTN = True
        
        t = time.localtime()
        
        if confirm:
            WriteIntoSaveFile(f"{t[2]}_{t[1]}_{t[0]}", f"{MoodTracker_Pile}", '/flash/libs/moodTracker.txt')
            MoodTracker_Num = 0
            ALLOW_SETTINGS_PAGE = True
            ALLOW_NEXT_PAGE = True
            OVERRIDE_NEXT_PAGE_BTN = False 
            OVERRIDE_SETTINGS_BTN = False  
            MoodTrackerPage()
            return
        
        imgs = [
            "/flash/res/img/Pile/PileHappy.png",
            "/flash/res/img/Pile/PileSmile.png",
            "/flash/res/img/Pile/PileIndifferent.png",
            "/flash/res/img/Pile/PileAngry.png",
            "/flash/res/img/Pile/PileFurious.png",
            ]
        
        if MoodTracker_Pile > len(imgs)-1:
            MoodTracker_Pile = 0
        elif MoodTracker_Pile < 0:
            MoodTracker_Pile = len(imgs)-1
        
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(1)
        M5.Lcd.setCursor(0, 190)
        M5.Lcd.print(f"Add mood for: \n{t[2]}_{t[1]}_{t[0]}")
        
        M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
        M5.Lcd.setTextSize(2)
        M5.Lcd.setCursor(40, 215)
        M5.Lcd.print(f"{mood[MoodTracker_Pile]}")
        
        M5.Lcd.drawPng(
            f"{imgs[MoodTracker_Pile]}",
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
        
    def pageMonthFeeling():
        global MoodTracker_Pile, MoodTracker_Num, ALLOW_SETTINGS_PAGE, ALLOW_NEXT_PAGE, OVERRIDE_NEXT_PAGE_BTN, OVERRIDE_SETTINGS_BTN
        
        ALLOW_SETTINGS_PAGE = False
        ALLOW_NEXT_PAGE = False
        OVERRIDE_NEXT_PAGE_BTN = True
        OVERRIDE_SETTINGS_BTN = True
        
        t=time.localtime()
        
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
            value=SearchSaveFile(key, '/flash/libs/moodTracker.txt')
            
            keyprev=f"{i-1}_{t[1]}_{t[0]}"
            valueprev=SearchSaveFile(keyprev, '/flash/libs/moodTracker.txt')
            
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
    
    pages = {
        0: page0,
        1: pageSetMood,
        2: pageMonthFeeling,
    }
    
    if MoodTracker_Num in pages:
        pages[MoodTracker_Num]()
    else:
        MoodTracker_Num = 0
        pages[MoodTracker_Num]()
        
def MoodTrackerPage_ButtonClick():
    global MoodTracker_Num
    MoodTracker_Num += 1
    MoodTrackerPage()
    
def MoodTrackerPage_ButtonHold():
    global MoodTracker_Num
    if MoodTracker_Num == 1:
        MoodTrackerPage(True)

def MoodTrackerPage_ButtonClick_LEFTBTN():
    global MoodTracker_Pile
    MoodTracker_Pile -= 1
    MoodTrackerPage()
    
def MoodTrackerPage_ButtonClick_RIGHTBTN():
    global MoodTracker_Pile
    MoodTracker_Pile += 1
    MoodTrackerPage()

## Chart creator
    ### ROW COLOR [POSITION, CLRS...] POSITION = false --> left; true --> right
def Chart(rows, cols, x=0, y=0, h=40, w=121, rowColors=None, columnColors=None, rowLetters=None, columnLetters=None, sortBy=None, size=4):
    
    localX, localY = x, y
    Column_Spacing = w // (cols - 1)
    Row_Spacing = h // (rows - 1)
    
    ## COLUMN CREATION
    for i in range(0, cols):
        if columnColors != None:
            if columnColors[0] == False:
                color = columnColors[i + 1] if i+1 < len(columnColors) else columnColors[1]
                M5.Lcd.fillEllipse(localX, y - size * 3, size, size, color)
            else:
                color = columnColors[i + 1] if i+1 < len(columnColors) else columnColors[1]
                M5.Lcd.fillEllipse(localX, y + h + size * 3, size, size, color)
        
        if columnLetters != None:
            if columnLetters[0] == False:
                letter = columnLetters[i + 1] if i+1 < len(columnLetters) else columnLetters[1]
                M5.Lcd.setTextSize(0.85)
                M5.Lcd.setTextColor(0xFFFFFF, 0X000000)
                M5.Lcd.setCursor(localX - len(letter) * 2, y - size * 2)
                M5.Lcd.print(letter)
            else:
                letter = columnLetters[i + 1] if i+1 < len(columnLetters) else columnLetters[1]
                M5.Lcd.setTextSize(0.85)
                M5.Lcd.setTextColor(0xFFFFFF, 0X000000)
                M5.Lcd.setCursor(localX - len(letter) * 2, y + h + size * 2)
                M5.Lcd.print(letter)
            
        M5.Lcd.drawLine(localX, y, localX, y + h, 0xBBBBBB)
        localX += Column_Spacing
    
    ## ROW CREATION
    for i in range(0, rows):
        if rowColors != None:
            if rowColors[0] == False:
                color = rowColors[i+1] if i+1 < len(rowColors) else rowColors[0]
                M5.Lcd.fillEllipse(x - size * 3, localY, size, size, color)
            else:
                color = rowColors[i+1] if i+1 < len(rowColors) else rowColors[0]
                M5.Lcd.fillEllipse(x + w + size * 3, localY, size, size, color)
                
            if rowLetters != None:
                if rowLetters[0] == False:
                    letter = rowLetters[i + 1] if i+1 < len(rowLetters) else rowLetters[1]
                    M5.Lcd.setTextSize(0.85)
                    M5.Lcd.setCursor(x - size * 3, localY - len(letter))
                    M5.Lcd.print(letter)
                else:
                    letter = rowLetters[i + 1] if i+1 < len(rowLetters) else rowLetters[1]
                    M5.Lcd.setTextSize(0.85)
                    M5.Lcd.setCursor(x + w + size * 3, localY - len(letter))
                    M5.Lcd.print(letter)
        M5.Lcd.drawLine(x, localY, x + w, localY, 0xBBBBBB)
        localY += Row_Spacing
        
    ## DATA ADDING
    pos = [] ## (x, y)
    for i, (key, value, specialkey) in enumerate(sortBy):
        key = int(key) if key.isdigit() else specialkey
        localX = x + Column_Spacing * int(key)
        localY = y + Row_Spacing * int(value)
        M5.Lcd.fillEllipse(localX, localY, size - 1, size - 1, 0xAA0099)
        pos.append((localX, localY))
        
        if i > 0 and i < len(sortBy):
            M5.Lcd.drawLine(pos[i - 1][0], pos[i - 1][1], pos[i][0], pos[i][1], 0xAA0099)

FindMyPage_LOOP_FUNCTIONS=None
FindMyPageNum=0
def FindMyPage():
    global clock, clocklabel, FindMyPage_LOOP_FUNCTIONS

    # --- Setup display ---
    M5.Lcd.clear(0x000000)
    M5.Lcd.fillRect(0, 0, M5.Lcd.width(), 20, 0xFFFFFF)
    clocklabel = Widgets.Label(clock, 0, 0, 1, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu18)

    # --- Circle data: [radius, r, spin, angle] ---
    circles = []
    
    pivot_x = 67
    pivot_y = 112

    def spawn_circle():
        dist = random.randint(35, 45)      # distance from pivot
        r = random.randint(1, 5)           # circle radius
        spin = random.uniform(0.1, 0.5)  # degrees per frame, small = slow
        angle = random.uniform(0, 360)     # initial angle
        circles.append([dist, r, spin, angle])

        # Draw initial circle
        x = int(pivot_x + dist * math.cos(math.radians(angle)))
        y = int(pivot_y + dist * math.sin(math.radians(angle)))
        M5.Lcd.fillCircle(x, y, r, 0xFFFFFF)

    def get_pos(dist, angle):
        rad = math.radians(angle)
        x = pivot_x + dist * math.cos(rad)
        y = pivot_y + dist * math.sin(rad)
        return int(x), int(y)

    def intro_Animation():
        M5.Lcd.setTextSize(2)
        M5.Lcd.setTextColor(0xFFFFFF, 0X000000)
        M5.Lcd.setCursor(40, 200)
        M5.Lcd.print("Find?")
        for c in circles:
            dist, r, spin, angle = c

            # Erase old position
            x, y = get_pos(dist, angle)
            M5.Lcd.fillCircle(x, y, r, 0x000000)

            # Update angle
            angle += spin
            if angle >= 360:
                angle -= 360
            c[3] = angle

            # Draw new position
            x, y = get_pos(dist, angle)
            M5.Lcd.fillCircle(x, y, r, 0xFFFFFF)
    
    into_called = False
    frame = 0
    def INTO_ARROW():
        nonlocal into_called, frame
        if not into_called:
            into_called = True
        else:
            return 0
        frames = [
                    '/flash/res/img/FindMyArrowIntroAnim/1.png',
                    '/flash/res/img/FindMyArrowIntroAnim/2.png',
                    '/flash/res/img/FindMyArrowIntroAnim/3.png',
                    '/flash/res/img/FindMyArrowIntroAnim/4.png',
                    ]
        pos=0
        while pos < 35:
            for c in circles:
                dist, r, spin, angle = c

                # Erase old position
                x, y = get_pos(dist, angle)
                if pos < 27:
                    M5.Lcd.fillCircle(x, y, r * 2, 0x000000)
                
                c[0] -= 1
                if pos > 25:
                    c[1] += 1
                # Update angle
                angle += spin * 3
                if angle >= 360:
                    angle -= 360
                c[3] = angle

                # Draw new position
                x, y = get_pos(dist, angle)
                M5.Lcd.fillCircle(x, y, r, 0xFFFFFF)
                
            if pos >= 31:
                M5.Lcd.drawPng(frames[frame], pivot_x - 25, pivot_y - 25)
                frame+=1
            pos+=1
        
        for c in circles:
            dist, r, spin, angle = c
            x, y = get_pos(dist, angle)
            M5.Lcd.fillCircle(x, y, r, 0x000000)
            
        M5.Lcd.drawPng('/flash/res/img/FindMyArrowIntroAnim/4.png', pivot_x - 25, pivot_y - 25)
        FindMyPageNum=3
    
    def approxLocaation_animation():
        M5.Lcd.setTextSize(2)
        M5.Lcd.setTextColor(0xFFFFFF, 0X000000)
        M5.Lcd.setCursor(0, 200)
        M5.Lcd.print("Locating \nphone...")
        
        ax, ay, az = tuple(round(x, 3) for x in M5.Imu.getAccel())
        
        for c in circles:
            dist, r, spin, angle = c

            # Erase old position
            x, y = get_pos(dist, angle)
            M5.Lcd.fillCircle(x, y, r, 0x000000)
            c[2] = ax
            # Update angle
            angle += spin
            if angle >= 360:
                angle -= 360
            c[3] = angle

            # Draw new position
            x, y = get_pos(dist, angle)
            M5.Lcd.fillCircle(x, y, r, 0xFFFFFF)
            
    def lookForPhone():
        nonlocal into_called, frame
        frame = 0
        into_called = False
        return 0
    
    FindMyPage_LOOP_FUNCTIONS = {
        0: intro_Animation,
        1: approxLocaation_animation,
        2: INTO_ARROW,
        3: lookForPhone,
    }
    
    for _ in range(20):
        spawn_circle()
    
def FindMyPage_LOOP_F():
    global FindMyPageNum, FindMyPage_LOOP_FUNCTIONS
    
    if FindMyPageNum in FindMyPage_LOOP_FUNCTIONS:
        FindMyPage_LOOP_FUNCTIONS[FindMyPageNum]()

def FindMyPage_ButtonClick():
    global FindMyPageNum
    
    if FindMyPageNum == 0:
        FindMyPageNum = 1
    elif FindMyPageNum == 1:
        FindMyPageNum = 2

quickOpen = False
settings_saveFile = "/flash/libs/settings_saveFile.txt"
QuickSettingsPage=0
## ime dugmeta ,(ukljucen/iskljucen, selektovan), (ukljucen funkcija, iskljucen funkcija), (AUDIO ON / AUDIO OFF)
## !// - Specijalni SUFIKS koji overriduje prikazivanje status settinga
## ? - NE CEKIRAJ SETTINGS SAVE FILE

buttons = [
    ("Audio", [False, True], (lambda: Speaker.setVolume(0), lambda: Speaker.setVolume(100)), ("Settings_Audio_Enable.wav", "Settings_Default_Disable.wav")),
    ("Bluetooth", [False, False], (None, None), ("Settings_Audio_Enable.wav", "Settings_Default_Disable.wav")),
    ("WiFi", [False, False], (lambda: network.WLAN(network.STA_IF).active(False), lambda: network.WLAN(network.STA_IF).active(True)), ("Settings_Audio_Enable.wav", "Settings_Default_Disable.wav")),
    ("?Power-Off!//", [False, False], (lambda: machine.deepsleep(), lambda: machine.deepsleep()), ("Settings_Audio_Enable.wav", "Settings_Default_Disable.wav")),
    ("?Reset!//", [False, False], (lambda: ResetDevice(), lambda: ResetDevice()), ("Settings_Audio_Enable.wav", "Settings_Default_Disable.wav")),
    ("?Settings!//", [True, False], (None, None), ("Settings_Audio_Enable.wav", "Settings_Default_Disable.wav")),
]
selectedIndex = 0
def QuickSettings(skip = False):
    global quickOpen, lastPage, currentPage, Pages, currentPageFunc, buttons, selectedIndex
    
    quickOpen = not quickOpen
    if not quickOpen and not skip:
        globals()[lastPage]()
        currentPageFunc = lastPage
        return
    else:
        lastPage = Pages[currentPage]
        currentPageFunc = 'QuickSettings'
        
    M5.Lcd.clear(0x000000)
    
    cols = 2
    cell_w = 70
    cell_h = 80
    
    for i, (name, (status, selected), _, _) in enumerate(buttons):
        col = i % cols
        row = i // cols

        x_img = col * cell_w + 2
        y_img = row * cell_h + 10   # 30 is starting y
        
        if not str.startswith(name, "?"):
            globalStatus = int(SearchSaveFile(name, settings_saveFile))
            status = bool(globalStatus)
        else:
            name = str.replace(name, "?", "")

        st = "ON" if status else "OFF"
        sel = "_Selected" if selected else ""
        showStat = True
        
        if str.endswith(name, "!//"):
            showStat = False
            name = str.replace(name, "!//", "")
        
        selColor = 0xff812f if selected else 0x000000

        M5.Lcd.drawPng(
            f"/flash/res/img/SettingsButtons/{name}{st}{sel}.png",
            x_img,
            y_img,
            0, 0,
            0, 0,
            1, 1
        )
        
        textStr = f": {st}" if showStat else ""

        Widgets.Label(
            f"{name}{textStr}",
            x_img,
            y_img + 60,
            0.6,
            0xFFFFFF,
            selColor,
            Widgets.FONTS.DejaVu18
        )

        #print(f"inserted {name}{i} into position {x_img},{y_img}")
        
def QuickSettings_ButtonClick():
    global buttons, selectedIndex
    prevIndex = selectedIndex
    selectedIndex += 1
    if selectedIndex >= len(buttons):
        selectedIndex = 0
    
    buttons[selectedIndex][1][1] = True
    buttons[prevIndex][1][1] = False
    QuickSettings(True)
    
def QuickSettings_ButtonHold():
    global buttons, selectedIndex
    val = not buttons[selectedIndex][1][0]
    buttons[selectedIndex][1][0] = val
    if buttons[selectedIndex][2][int(val)]:
        buttons[selectedIndex][2][int(val)]()
    if not str.startswith(buttons[selectedIndex][0], "?"):
        WriteIntoSaveFile(buttons[selectedIndex][0], f"{int(val)}", settings_saveFile)
        
    QuickSettings(True)
    time.sleep(0.5)
    '''if buttons[selectedIndex][1][0] and buttons[selectedIndex][1][1]:
        play_audio(buttons[selectedIndex][3][0])
    elif not buttons[selectedIndex][1][0] and buttons[selectedIndex][1][1]:
        play_audio(buttons[selectedIndex][3][1])'''
    
def HomePage_ButtonHold():
    global stepCount, currentPage, stepGoal_label
    stepCount = stepCount + 10
    if currentPage == 0:
        stepGoal_label.setText(f"{stepCount}")
        M5.Lcd.drawPng(
            f"/flash/res/img/Bars_HomePage/Bar{PercentageBar()}.png",
            0,
            190,
            0, 0,
            0, 0,
            0.7, 0.7
        )
    elif currentPage == 1:
        stepGoal_label = Widgets.Label(f"{stepCount}/{stepGoal}", 15, 160, 1, 0x15616d, 0x000000, Widgets.FONTS.DejaVu18)

keyboard_LOOP_FUNCTIONS=None
keyboard_sel_func=0

lowercase = [chr(i) for i in range(ord('a'), ord('z') + 1)]
lowercase.append(" ")
uppercase = [c.upper() for c in lowercase]
numberkb = [str(i) for i in range(0, 10)]
special_characters = list("!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~")

keybIndex=0
keybChoices=[lowercase, uppercase, special_characters, numberkb]
keyb=lowercase

selected_character=0
last_char=0

word=""

# PRESET VALUE OF KEYBOARD WHICH IT WILL USE
# XtoSet je promenljiva koja ce dobiti promenu tu word stvar
def keyboard(allow_different = True, preset = 0, XtoSet=None):
    global ALLOW_SETTINGS_PAGE, ALLOW_NEXT_PAGE, OVERRIDE_NEXT_PAGE_BTN, OVERRIDE_SETTINGS_BTN, keyboard_LOOP_FUNCTIONS
    global lastPage, currentPage, Pages, currentPageFunc
    global keybIndex, keybChoices, keyb, word
    
    ALLOW_NEXT_PAGE=False
    ALLOW_SETTINGS_PAGE=False
    OVERRIDE_NEXT_PAGE_BTN=True
    OVERRIDE_SETTINGS_BTN=True
    
    lastPage = Pages[currentPage]
    currentPageFunc = 'keyboard'
    
    M5.Lcd.fillRect(0, 40, 135, 200, 0x000000)
    M5.Lcd.fillRect(0, 0, 135, 40, 0x555555)
    
    selected_character=0
    word=""
    
    keybIndex=preset
    keyb=keybChoices[keybIndex]
    
    xInc=20
    yInc=35
    
    def Load():
        global keyb, word
        x=0
        y=45
        
        # redraw the black bg in case a new kb is drawn
        M5.Lcd.fillRect(0, 40, 135, 200, 0x000000)
        M5.Lcd.fillRect(0, 0, 135, 40, 0x555555)
        
        Widgets.Label(
                word,
                0,
                10,
                1.3,
                0XFFFFFF,
                0x555555,
                Widgets.FONTS.DejaVu18
            )
        
        M5.Lcd.drawPng(
            "/flash/res/img/misc/KeyboardBtns.png",
            0,
            205,
            0, 0,
            0, 0,
            1, 1
        )
        
        for i, v in enumerate(keyb, 1):
            Widgets.Label(
                f"{v}",
                x,
                y,
                1.3,
                0XFFFFFF,
                0x000000,
                Widgets.FONTS.DejaVu18
            )
            x+=xInc
            if i % 7 == 0:
                y+=yInc
                x=0
        
        selected_character=0
        last_char=0
        
        UpdateChar()
    
    def UpdateChar():
        global selected_character, last_char
        global keyb
        
        x=0
        y=0
        
        if selected_character > len(keyb) - 1:
            selected_character = 0
        elif selected_character < 0:
            selected_character = len(keyb) - 1
        
        def calcPos(indexLocal):
            x=0
            y=45
            for i in range(1, indexLocal + 1):
                x+=xInc
                if i % 7 == 0:
                    y+=yInc
                    x=0
            return x, y

        # recoloring prev pos
        x,y = calcPos(last_char)
        Widgets.Label(
                f"{keyb[last_char]}",
                x,
                y,
                1.3,
                0XFFFFFF,
                0x000000,
                Widgets.FONTS.DejaVu18
            )
        # coloring this one
        x,y = calcPos(selected_character)
        Widgets.Label(
                f"{keyb[selected_character]}",
                x,
                y,
                1.3,
                0XFFFFFF,
                0xff812f,
                Widgets.FONTS.DejaVu18
            )
        
        last_char = selected_character
    
    def addChar():
        global word, selected_character
        global keyb
        
        char = keyb[selected_character]
        word+=char
        
        Widgets.Label(
                word,
                0,
                10,
                1.3,
                0XFFFFFF,
                0x555555,
                Widgets.FONTS.DejaVu18
            )
    
    def rmvChar():
        global word
        
        if len(word) > 0:
            word = word[:-1]
            
            M5.Lcd.fillRect(0, 0, 135, 40, 0x555555)
            
            Widgets.Label(
                word,
                0,
                10,
                1.3,
                0XFFFFFF,
                0x555555,
                Widgets.FONTS.DejaVu18
            )
            
    def setKeyb():
        global keybIndex, keybChoices, keyb
        if allow_different:
            keybIndex = keybIndex + 1 if keybIndex < len(keybChoices) - 1 else 0
            
            keyb = keybChoices[keybIndex]
            Load()
            
    def setX():
        global ALLOW_SETTINGS_PAGE, ALLOW_NEXT_PAGE, OVERRIDE_NEXT_PAGE_BTN, OVERRIDE_SETTINGS_BTN
        global lastPage, currentPage, Pages, currentPageFunc, word
        
        if XtoSet is not None:
            saved_type = type(globals()[XtoSet])

            globals()[XtoSet] = saved_type(word)

            if SearchSaveFile(XtoSet) is not None:
                WriteIntoSaveFile(XtoSet, word)
        
        ALLOW_NEXT_PAGE=True
        ALLOW_SETTINGS_PAGE=True 
        OVERRIDE_NEXT_PAGE_BTN=False 
        OVERRIDE_SETTINGS_BTN=False
        
        currentPageFunc = lastPage
        globals()[lastPage]()
        
    keyboard_LOOP_FUNCTIONS = {
        0: Load,
        1: UpdateChar,
        2: addChar,
        3: rmvChar,
        4: setKeyb,
        5: setX
    }
    
    Load()

def keyboard_ButtonClick_RIGHTBTN():
    global keyboard_LOOP_FUNCTIONS, selected_character
    
    selected_character+=1
    
    keyboard_LOOP_FUNCTIONS[1]()
    
def keyboard_ButtonHold_RIGHTBTN():
    global keyboard_LOOP_FUNCTIONS
    
    keyboard_LOOP_FUNCTIONS[4]()
    time.sleep(0.1)
    
def keyboard_ButtonClick_LEFTBTN():
    global keyboard_LOOP_FUNCTIONS, selected_character
    keyboard_LOOP_FUNCTIONS[3]()
    
def keyboard_ButtonClick():
    global keyboard_LOOP_FUNCTIONS
    keyboard_LOOP_FUNCTIONS[2]()
    
def keyboard_ButtonHold():
    global keyboard_LOOP_FUNCTIONS
    keyboard_LOOP_FUNCTIONS[5]()

PageSelectedIndex=0
pageSelectionEntered=False
def PageSelection():
    global Pages, currentPage, currentPageFunc, pageSelectionEntered, PageSelectedIndex, ALLOW_SETTINGS_PAGE, ALLOW_NEXT_PAGE, OVERRIDE_NEXT_PAGE_BTN
    
    if not pageSelectionEntered:
        nextpage_overlay(True, SelectionPage_IntroFrames)
        pageSelectionEntered=True
        currentPage='PageSelection'
        currentPageFunc='PageSelection'
        ALLOW_NEXT_PAGE=False
        ALLOW_SETTINGS_PAGE=False
        OVERRIDE_NEXT_PAGE_BTN=True 
        
    if PageSelectedIndex > len(Pages) - 1:
        PageSelectedIndex = 0
    
    def PageList():
        y=0
        w=135
        h=25
        TextSize=1.5
        for i, page in enumerate(Pages):
            name = page.replace("Page", "")
            if i != PageSelectedIndex:
                M5.Lcd.drawRect(0, y, w, h, 0xff812f)
                M5.Lcd.setCursor(0, y+5)
                M5.Lcd.setTextSize(TextSize)
                M5.Lcd.setTextColor(0xff812f, 0X000000)
                M5.Lcd.print(f"{name}")
            else:
                M5.Lcd.fillRect(0, y, w, h, 0xff812f)
                M5.Lcd.setCursor(0, y+5)
                M5.Lcd.setTextSize(TextSize)
                M5.Lcd.setTextColor(0xFFFFFF, 0xff812f)
                M5.Lcd.print(f"{name}")
                
            y+=h
                
    M5.Lcd.clear(0x000000)
    PageList()

def PageSelection_ButtonClick_RIGHTBTN():
    global PageSelectedIndex
    PageSelectedIndex+=1
    PageSelection()

def PageSelection_ButtonHold_RIGHTBTN():
    global Pages, currentPage, currentPageFunc, pageSelectionEntered, PageSelectedIndex, pageSelectionEntered, ALLOW_NEXT_PAGE, ALLOW_SETTINGS_PAGE, OVERRIDE_NEXT_PAGE_BTN
    selPage=Pages[PageSelectedIndex]
    frames = PageGenie_Frames
        
    x = 0
    y = -240//2 + (PageSelectedIndex + 1)*25 - 5
    
    for i, frame in enumerate(frames):
        if i < 3:
            M5.Lcd.drawPng(frame, x, y)
        else:
            t = 0.25  # tween speed (0.1 slow → 0.4 fast)

            x = lerp(x, 0, t)
            y = lerp(y, 0, t)

            M5.Lcd.drawPng(frame, int(x), int(y))
    
    currentPage = PageSelectedIndex
    currentPageFunc = selPage
    PageSelectedIndex=0
    pageSelectionEntered=False
    ALLOW_NEXT_PAGE=True 
    ALLOW_SETTINGS_PAGE=True
    OVERRIDE_NEXT_PAGE_BTN=False  
    globals()[selPage]()
 
def lerp(a, b, t):
    return a + (b - a) * t

def updateClock():
    global clock
    if clocklabel == None: return
    clock = f"{TIME[3]:02d}:{TIME[4]:02d}"
    clocklabel.setText(clock)
    
def PercentageBar():
    percent = (stepCount / stepGoal) * 100

    # map percent → 0,25,50,75,100
    step = int(percent / 25) * 25

    # clamp safely
    return max(0, min(100, step))


NextPage_Imgs = [
    '/flash/res/img/NextPageFrames/1.png',
    '/flash/res/img/NextPageFrames/2.png',
    '/flash/res/img/NextPageFrames/3.png',
    '/flash/res/img/NextPageFrames/4.png',
    '/flash/res/img/NextPageFrames/5.png',
    '/flash/res/img/NextPageFrames/6.png',
]

SelectionPage_IntroFrames = [
    '/flash/res/img/SelectionPage_IntroFrames/2.png',
    '/flash/res/img/SelectionPage_IntroFrames/3.png',
    '/flash/res/img/SelectionPage_IntroFrames/4.png',
    '/flash/res/img/SelectionPage_IntroFrames/6.png',
    '/flash/res/img/SelectionPage_IntroFrames/7.png',
]

PageGenie_Frames = [
    '/flash/res/img/PageGenie/1.png',
    '/flash/res/img/PageGenie/2.png',
    '/flash/res/img/PageGenie/3.png',
    '/flash/res/img/PageGenie/4.png',
    '/flash/res/img/PageGenie/5.png',
    '/flash/res/img/PageGenie/6.png',
]

def nextpage_overlay(expand=True, imgList=NextPage_Imgs):
    frames = imgList if expand else list(reversed(imgList))
    for frame in frames:
        M5.Lcd.drawPng(frame, 0, 0)

MsgBubble_Imgs = [
    '/flash/res/img/MsgBubble/1.png',
    '/flash/res/img/MsgBubble/2.png',
    '/flash/res/img/MsgBubble/3.png',
    '/flash/res/img/MsgBubble/4.png',
    '/flash/res/img/MsgBubble/5.png',
    '/flash/res/img/MsgBubble/6.png',
    '/flash/res/img/MsgBubble/7.png',
    '/flash/res/img/MsgBubble/8.png',
    '/flash/res/img/MsgBubble/9.png',
]

def Msg_Overlay(expand=True, Message="", sleep_tm=2, notif="Notification_Default.wav"):
    global MsgBubble_Imgs, lastPage, Pages, currentPage
    
    lastPage = Pages[currentPage]
    frames = MsgBubble_Imgs if expand else list(reversed(MsgBubble_Imgs))
    for frame in frames:
        M5.Lcd.drawPng(frame, 0, 0)
    M5.Lcd.setTextColor(0xFFFFFF, 0xFFFFFF)
    M5.Lcd.setTextSize(1.3)
    M5.Lcd.setCursor(15, 35)
    M5.Lcd.print(Message)
    #Speaker.playWavFile(soundsStartPos + notif)
    time.sleep(sleep_tm)
    globals()[lastPage]()

def play_audio(file_path):
    global speaker
    full_path = soundsStartPos + file_path
    
    Speaker.playWavFile(full_path, 0, -1, True)
        
def changepage(next=True):
    global currentPage, Pages, currentPageFunc

    if next:
        currentPage += 1
        if currentPage >= len(Pages):
            currentPage = 0
    else:
        currentPage -= 1
        if currentPage < 0:
            currentPage = len(Pages) - 1
            
    func_name = Pages[currentPage]
    nextpage_overlay()
    
    Speaker.tone(1500, 5)
    currentPageFunc = func_name
    globals()[func_name]()
    
def SearchSaveFile(Name, file=saveFile):
    inside_block = False
    result = []

    with open(file) as f:
        for line in f:
            line = line.strip()

            # Start of block
            if line == Name + "=[":
                inside_block = True
                continue

            # Normal key=value (only if not in a block)
            if not inside_block and line.startswith(Name + "="):
                return line.split("=", 1)[1]

            # Inside block
            if inside_block:
                if line == "]":
                    return result
                if "=" in line:
                    k, v = line.split("=", 1)
                    result.append((k.strip(), v.strip()))

    return None

def WriteIntoSaveFile(Name, new_value, File=saveFile):
    """
    Writes a value into saveFile.
    - new_value can be:
        - a string/int/etc. for a normal key=value
        - a dict for a block-style entry (Name=[key=value...])
    """
    tmp_name = File + ".tmp"
    found = False

    # Determine type
    is_block = isinstance(new_value, dict)

    with open(File, "r") as src, open(tmp_name, "w") as tmp:
        inside_block = False

        for line in src:
            stripped = line.strip()

            # Check if we're entering a block
            if stripped == f"{Name}=[":
                found = True
                inside_block = True
                tmp.write(f"{Name}=[\n")

                # Write the new block content
                if is_block:
                    for k, v in new_value.items():
                        tmp.write(f"{k}={v}\n")
                else:
                    tmp.write(f"value={new_value}\n")

                # Skip old block lines
                continue

            # Skip old block lines
            if inside_block:
                if stripped == "]":
                    inside_block = False
                continue

            # Handle normal key=value lines
            if not inside_block and stripped.startswith(Name + "="):
                found = True
                if not is_block:
                    tmp.write(f"{Name}={new_value}\n")
                else:
                    tmp.write(f"{Name}=[\n")
                    for k, v in new_value.items():
                        tmp.write(f"{k}={v}\n")
                    tmp.write("]\n")
                continue

            # Otherwise, copy line as-is
            tmp.write(line)

        # If not found, append at the end
        if not found:
            if is_block:
                tmp.write(f"{Name}=[\n")
                for k, v in new_value.items():
                    tmp.write(f"{k}={v}\n")
                tmp.write("]\n")
            else:
                tmp.write(f"{Name}={new_value}\n")

    # Replace old file safely (MicroPython-compatible)
    try:
        os.remove(File)
    except OSError:
        pass
    os.rename(tmp_name, File)

def acelGyroTest():
    ax, ay, az = tuple(round(x, 2) for x in M5.Imu.getAccel())
    gx, gy, gz = tuple(round(x, 2) for x in M5.Imu.getGyro())
    #print("Accel:", ax, ay, az)
    print("Gyro:", gx, gy, gz)
    
    time.sleep(0.1)

def ResetDevice():
    WriteIntoSaveFile("WENT_THROUGH_SETUP", "False")
    WriteIntoSaveFile("height", "0")
    WriteIntoSaveFile("weight", "0")
    WriteIntoSaveFile("age", "0")
    WriteIntoSaveFile("Timezone", "0")
    WriteIntoSaveFile("UTC", "none")
    machine.reset()

def loop():
    global frame, currentPageFunc, goalReached
    M5.update()
    updateClock()
    #acelGyroTest()
    
    globalfunc_name = f"{currentPageFunc}_LOOP_F"
    if globalfunc_name in globals():
        globals()[globalfunc_name]()
    
    if stepCount >= stepGoal and not goalReached:
        Msg_Overlay(True, "You've reached\n your goal!")
        goalReached = True
    
    if BtnA.isHolding():
        func_name = f"{currentPageFunc}_ButtonHold"
        if func_name in globals():
            globals()[func_name]()
        
    if BtnA.wasClicked():
        func_name = f"{currentPageFunc}_ButtonClick"
        if func_name in globals():
            globals()[func_name]()
        
    if BtnB.wasClicked():
        if ALLOW_NEXT_PAGE:
            changepage()
        elif OVERRIDE_NEXT_PAGE_BTN and not ALLOW_NEXT_PAGE:
            func_name = f"{currentPageFunc}_ButtonClick_RIGHTBTN"
            if func_name in globals():
                globals()[func_name]()
                
    if BtnB.isHolding():
        if OVERRIDE_NEXT_PAGE_BTN:
            func_name = f"{currentPageFunc}_ButtonHold_RIGHTBTN"
            if func_name in globals():
                globals()[func_name]()
        else:
            PageSelection()
        
    if BtnPWR.wasClicked():
        if ALLOW_SETTINGS_PAGE:
            QuickSettings()
        elif OVERRIDE_SETTINGS_BTN and not ALLOW_SETTINGS_PAGE:
            func_name = f"{currentPageFunc}_ButtonClick_LEFTBTN"
            if func_name in globals():
                globals()[func_name]()
        
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