import os, sys, io, time, ntptime, network, random, machine, math
import uasyncio as asyncio
import M5
from M5 import *

import GlobalVars
from SaveFileModule import FileManager
from Keyboard import keyboard

TIME = time.localtime() 

soundsStartPos = "/flash/res/audio/"
speaker = None

saveFile = "/flash/libs/data.txt"

Pages = ['HomePage', 'FitnessPage', 'MoodTrackerPage', 'FindMyPage', 'Calendar']
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

def setup():
    global speaker, weight, height, TIME
    M5.begin()
    Widgets.fillScreen(0xFFFFFF)
    Widgets.setRotation(0)
    
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
    
    if FileManager.search("WENT_THROUGH_SETUP") == "False":
        SetupPage()
    else:
        weight = int(FileManager.search("weight"))
        height = int(FileManager.search("height"))
        
        HomePage()
    
    globalStatus = int(FileManager.search('Audio', "/flash/libs/settings_saveFile.txt"))
    Speaker.setVolume(100 * globalStatus)
    Speaker.tone(7000, 50)
    time.sleep(0.1)
    Speaker.tone(9000, 50)
    time.sleep(0.1)
    Speaker.tone(10600, 100)
    
    speaker = M5.createSpeaker()
    speaker.begin()

from Home_Page import HomePage as HP
def HomePage():
    GlobalVars.currentPageModule = HP()

from Fitness_page import Fitness
def FitnessPage():
    GlobalVars.currentPageModule = Fitness()

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

from MoodTracker_page import MoodTrackerApp as MTA
def MoodTrackerPage():
    GlobalVars.currentPageModule = MTA()

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

from Calendar import Calendar as CAL
def Calendar():
    GlobalVars.currentPageModule = CAL()

from QuickSettings import QuickSettings as QS
def QuickSettings():
    GlobalVars.quickOpen = not GlobalVars.quickOpen

    if GlobalVars.quickOpen:
        GlobalVars.currentPageModule = QS()
    else:
        GlobalVars.currentPageModule.close()

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
        
def changepage(_next=True):
    global currentPage, Pages, currentPageFunc

    if _next:
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
        elif hasattr(GlobalVars.currentPageModule, "ButtonHold"):
            getattr(GlobalVars.currentPageModule, "ButtonHold")()
    
    if BtnA.wasHold():
        func_name = f"{currentPageFunc}_ButtonWasHold"
        if func_name in globals():
            globals()[func_name]()
        elif hasattr(GlobalVars.currentPageModule, "wasHold"):
            getattr(GlobalVars.currentPageModule, "wasHold")()
        
    if BtnA.wasClicked():
        func_name = f"{currentPageFunc}_ButtonClick"
        if func_name in globals():
            globals()[func_name]()
        elif hasattr(GlobalVars.currentPageModule, "ButtonClick"):
            getattr(GlobalVars.currentPageModule, "ButtonClick")()
        
    if BtnB.wasClicked():
        if GlobalVars.ALLOW_NEXT_PAGE:
            changepage()
        elif GlobalVars.OVERRIDE_NEXT_PAGE_BTN and not GlobalVars.ALLOW_NEXT_PAGE:
            func_name = f"{currentPageFunc}_ButtonClick_RIGHTBTN"
            if func_name in globals():
                globals()[func_name]()
            elif hasattr(GlobalVars.currentPageModule, "ButtonClick_RIGHTBTN"):
                getattr(GlobalVars.currentPageModule, "ButtonClick_RIGHTBTN")()
                
    if BtnB.isHolding():
        if GlobalVars.OVERRIDE_NEXT_PAGE_BTN:
            func_name = f"{currentPageFunc}_ButtonHold_RIGHTBTN"
            if func_name in globals():
                globals()[func_name]()
            elif hasattr(GlobalVars.currentPageModule, "ButtonHold_RIGHTBTN"):
                getattr(GlobalVars.currentPageModule, "ButtonHold_RIGHTBTN")()
        else:
            PageSelection()
        
    if BtnPWR.wasClicked():
        if GlobalVars.ALLOW_SETTINGS_PAGE:
            QuickSettings()
        elif GlobalVars.OVERRIDE_SETTINGS_BTN and not GlobalVars.ALLOW_SETTINGS_PAGE:
            func_name = f"{currentPageFunc}_ButtonClick_LEFTBTN"
            if func_name in globals():
                globals()[func_name]()
            elif hasattr(GlobalVars.currentPageModule, "ButtonClick_LEFTBTN"):
                getattr(GlobalVars.currentPageModule, "ButtonClick_LEFTBTN")()
        
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