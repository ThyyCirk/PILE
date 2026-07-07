## SETTINGS PAGE DONT DELETE

## ime dugmeta ,(ukljucen/iskljucen, selektovan), (ukljucen funkcija, iskljucen funkcija), (AUDIO ON / AUDIO OFF)
## !// - Specijalni SUFIKS koji overriduje prikazivanje status settinga
## ? - NE CEKIRAJ SETTINGS SAVE FILE

import M5
from M5 import *
import time
from SaveFileModule import FileManager
import GlobalVars
import os, network, machine

class QuickSettings:

    def __init__(self):
        if not GlobalVars.quickOpen:
            self.close()
            return

        self.settings_saveFile = "/flash/libs/settings_saveFile.txt"
        self.QuickSettingsPage = 0

        self.buttons = [
            ("Audio", [False, True], (lambda: Speaker.setVolume(0), lambda: Speaker.setVolume(100)), ("Settings_Audio_Enable.wav", "Settings_Default_Disable.wav")),
            ("Bluetooth", [False, False], (None, None), ("Settings_Audio_Enable.wav", "Settings_Default_Disable.wav")),
            ("WiFi", [False, False], (lambda: network.WLAN(network.STA_IF).active(False), lambda: network.WLAN(network.STA_IF).active(True)), ("Settings_Audio_Enable.wav", "Settings_Default_Disable.wav")),
            ("?Power-Off!//", [False, False], (lambda: machine.deepsleep(), lambda: machine.deepsleep()), ("Settings_Audio_Enable.wav", "Settings_Default_Disable.wav")),
            ("?Reset!//", [False, False], (lambda: self.ResetDevice(), lambda: self.ResetDevice()), ("Settings_Audio_Enable.wav", "Settings_Default_Disable.wav")),
            ("?Settings!//", [True, False], (None, None), ("Settings_Audio_Enable.wav", "Settings_Default_Disable.wav")),
        ]
        self.selectedIndex = 0
        GlobalVars.lastPageModule = type(GlobalVars.currentPageModule) if GlobalVars.currentPageModule else None
        GlobalVars.currentPageModule = self
        self.QuickSettings()

    def __call__(self):
        if GlobalVars.quickOpen:
            self.QuickSettings()
        else:
            self.close()

    def QuickSettings(self):
        GlobalVars.topBarVisible = False
        
        GlobalVars.ALLOW_NEXT_PAGE=False
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN=True 

        M5.Lcd.clear(0x000000)

        if not GlobalVars.quickOpen:
            self.close()
            return

        cols = 2
        cell_w = 70
        cell_h = 80

        for i, (name, (status, selected), _, _) in enumerate(self.buttons):
            col = i % cols
            row = i // cols

            x_img = col * cell_w + 2
            y_img = row * cell_h + 10   # 30 is starting y

            if not str.startswith(name, "?"):
                globalStatus = int(FileManager.search(name, self.settings_saveFile))
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
    
    def ResetDevice():
        FileManager.write("WENT_THROUGH_SETUP", "False")
        FileManager.write("height", "0")
        FileManager.write("weight", "0")
        FileManager.write("age", "0")
        FileManager.write("Timezone", "0")
        FileManager.write("UTC", "none")
        machine.reset()

    def close(self):
        GlobalVars.ALLOW_NEXT_PAGE=True 
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN=False
        if GlobalVars.lastPageModule is not None:
            GlobalVars.currentPageModule = GlobalVars.lastPageModule()
        else:
            from Home_Page import Home_Page
            GlobalVars.currentPageModule = Home_Page()
        

    def ButtonClick(self):
        prevIndex = self.selectedIndex
        self.selectedIndex += 1
        if self.selectedIndex >= len(self.buttons):
            self.selectedIndex = 0

        self.buttons[self.selectedIndex][1][1] = True
        self.buttons[prevIndex][1][1] = False
        self.QuickSettings()

    def ButtonHold(self):
        val = not self.buttons[self.selectedIndex][1][0]
        self.buttons[self.selectedIndex][1][0] = val
        if self.buttons[self.selectedIndex][2][int(val)]:
            self.buttons[self.selectedIndex][2][int(val)]()
        if not str.startswith(self.buttons[self.selectedIndex][0], "?"):
            FileManager.write(self.buttons[self.selectedIndex][0], f"{int(val)}", self.settings_saveFile)

        self.QuickSettings()
        time.sleep(0.5)
        '''if buttons[selectedIndex][1][0] and buttons[selectedIndex][1][1]:
            play_audio(buttons[selectedIndex][3][0])
        elif not buttons[selectedIndex][1][0] and buttons[selectedIndex][1][1]:
            play_audio(buttons[selectedIndex][3][1])'''