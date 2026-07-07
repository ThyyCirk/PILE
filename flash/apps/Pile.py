import time
import M5
from M5 import *

import network, ntptime 

import GlobalVars
from SaveFileModule import FileManager
from TopBar import TopBar
import AppsModule

soundsStartPos = "/flash/res/audio/"
speaker = None

topBarInstance = None

def setup():
    global topBarInstance
    M5.begin()
    M5.Lcd.clear(0x000000)
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
    
    topBarInstance = TopBar()
    
    if FileManager.search("WENT_THROUGH_SETUP") == "False":
        from Setup import Setup
        GlobalVars.currentPageModule = Setup()
    else:
        from Home_Page import Home_Page as HP
        GlobalVars.currentPageModule = HP()
    
    globalStatus = int(FileManager.search('Audio', "/flash/libs/settings_saveFile.txt"))
    Speaker.setVolume(100 * globalStatus)
    Speaker.tone(7000, 50)
    time.sleep(0.1)
    Speaker.tone(9000, 50)
    time.sleep(0.1)
    Speaker.tone(10600, 100)
    
    speaker = M5.createSpeaker()
    speaker.begin()

from QuickSettings import QuickSettings as QS
def QuickSettings():
    GlobalVars.quickOpen = not GlobalVars.quickOpen

    if GlobalVars.quickOpen:
        GlobalVars.currentPageModule = QS()
    else:
        GlobalVars.currentPageModule.close()

def PageSelection():
    GlobalVarscurrentPageModule = AppsModule.Apps()

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
    AppsModule.changepage(_next)

def acelGyroTest():
    ax, ay, az = tuple(round(x, 2) for x in M5.Imu.getAccel())
    gx, gy, gz = tuple(round(x, 2) for x in M5.Imu.getGyro())
    #print("Accel:", ax, ay, az)
    print("Gyro:", gx, gy, gz)
    
    time.sleep(0.1)

def loop():
    global topBarInstance
    M5.update()
    #acelGyroTest()
        
    if hasattr(GlobalVars.currentPageModule, "tick"):
        GlobalVars.currentPageModule.tick()
    
    if BtnA.isHolding():
        if hasattr(GlobalVars.currentPageModule, "ButtonHold"):
            getattr(GlobalVars.currentPageModule, "ButtonHold")()
    
    if BtnA.wasHold():
        if hasattr(GlobalVars.currentPageModule, "wasHold"):
            getattr(GlobalVars.currentPageModule, "wasHold")()
        
    if BtnA.wasClicked():
        if hasattr(GlobalVars.currentPageModule, "ButtonClick"):
            getattr(GlobalVars.currentPageModule, "ButtonClick")()
        
    if BtnB.wasClicked():
        if GlobalVars.ALLOW_NEXT_PAGE:
            changepage()
        elif GlobalVars.OVERRIDE_NEXT_PAGE_BTN and not GlobalVars.ALLOW_NEXT_PAGE:
            if hasattr(GlobalVars.currentPageModule, "ButtonClick_RIGHTBTN"):
                getattr(GlobalVars.currentPageModule, "ButtonClick_RIGHTBTN")()
                
    if BtnB.isHolding():
        if GlobalVars.OVERRIDE_NEXT_PAGE_BTN:
            if hasattr(GlobalVars.currentPageModule, "ButtonHold_RIGHTBTN"):
                getattr(GlobalVars.currentPageModule, "ButtonHold_RIGHTBTN")()
        else:
            PageSelection()
        
    if BtnPWR.wasClicked():
        if GlobalVars.ALLOW_SETTINGS_PAGE:
            QuickSettings()
        elif GlobalVars.OVERRIDE_SETTINGS_BTN and not GlobalVars.ALLOW_SETTINGS_PAGE:
            if hasattr(GlobalVars.currentPageModule, "ButtonClick_LEFTBTN"):
                getattr(GlobalVars.currentPageModule, "ButtonClick_LEFTBTN")()
    
    topBarInstance.tick()
        
if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        M5.Lcd.setTextSize(1)
        M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
        try:
            from utility import print_error_msg
            print_error_msg(e)
        except:
            print(e)
