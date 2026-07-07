import GlobalVars
import M5
from M5 import *
import time
from SaveFileModule import FileManager

lowercase = [chr(i) for i in range(ord('a'), ord('z') + 1)]
lowercase.append(" ")
uppercase = [c.upper() for c in lowercase]
numberkb = [str(i) for i in range(0, 10)]
special_characters = list("!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~")

# PRESET VALUE OF KEYBOARD WHICH IT WILL USE
# XtoSet je promenljiva koja ce dobiti promenu tu word stvar


class keyboard:
    def __init__(self, allow_different=True, preset=0, XtoSet=None):
        self.allow_different = allow_different
        self.XtoSet = XtoSet

        self.keybChoices = [lowercase, uppercase, special_characters, numberkb]
        self.keybIndex = preset
        self.keyb = self.keybChoices[self.keybIndex]

        self.selected_character = 0
        self.last_char = 0
        self.word = ""

        self.xInc = 20
        self.yInc = 35
        
        GlobalVars.lastPageModule = GlobalVars.currentPageModule
        print(f"last module : {GlobalVars.lastPageModule}")
        GlobalVars.currentPageModule = self

        GlobalVars.ALLOW_NEXT_PAGE = False
        GlobalVars.ALLOW_SETTINGS_PAGE = False
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN = True
        GlobalVars.OVERRIDE_SETTINGS_BTN = True

        self.Load()

    def Load(self):
        # redraw the black bg in case a new kb is drawn
        M5.Lcd.fillRect(0, 40, 135, 200, 0x000000)
        M5.Lcd.fillRect(0, 0, 135, 40, 0x555555)

        Widgets.Label(
            self.word,
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

        x = 0
        y = 45
        for i, v in enumerate(self.keyb, 1):
            Widgets.Label(
                f"{v}",
                x,
                y,
                1.3,
                0XFFFFFF,
                0x000000,
                Widgets.FONTS.DejaVu18
            )
            x += self.xInc
            if i % 7 == 0:
                y += self.yInc
                x = 0

        self.selected_character = 0
        self.last_char = 0

        self.UpdateChar()

    def calcPos(self, indexLocal):
        x = 0
        y = 45
        for i in range(1, indexLocal + 1):
            x += self.xInc
            if i % 7 == 0:
                y += self.yInc
                x = 0
        return x, y

    def UpdateChar(self):
        if self.selected_character > len(self.keyb) - 1:
            self.selected_character = 0
        elif self.selected_character < 0:
            self.selected_character = len(self.keyb) - 1

        # recoloring prev pos
        x, y = self.calcPos(self.last_char)
        Widgets.Label(
            f"{self.keyb[self.last_char]}",
            x,
            y,
            1.3,
            0XFFFFFF,
            0x000000,
            Widgets.FONTS.DejaVu18
        )
        # coloring this one
        x, y = self.calcPos(self.selected_character)
        Widgets.Label(
            f"{self.keyb[self.selected_character]}",
            x,
            y,
            1.3,
            0XFFFFFF,
            0xff812f,
            Widgets.FONTS.DejaVu18
        )

        self.last_char = self.selected_character

    def addChar(self):
        char = self.keyb[self.selected_character]
        self.word += char

        Widgets.Label(
            self.word,
            0,
            10,
            1.3,
            0XFFFFFF,
            0x555555,
            Widgets.FONTS.DejaVu18
        )

    def rmvChar(self):
        if len(self.word) > 0:
            self.word = self.word[:-1]

            M5.Lcd.fillRect(0, 0, 135, 40, 0x555555)

            Widgets.Label(
                self.word,
                0,
                10,
                1.3,
                0XFFFFFF,
                0x555555,
                Widgets.FONTS.DejaVu18
            )

    def setKeyb(self):
        if self.allow_different:
            self.keybIndex = self.keybIndex + 1 if self.keybIndex < len(self.keybChoices) - 1 else 0

            self.keyb = self.keybChoices[self.keybIndex]
            self.Load()

    def setX(self):
        if self.XtoSet is not None:
            saved_type = type(self.XtoSet)
        
        
        if FileManager.search(self.XtoSet) is not None:
            print(self.XtoSet, self.word)
            FileManager.write(self.XtoSet, self.word)

        GlobalVars.ALLOW_NEXT_PAGE = True
        GlobalVars.ALLOW_SETTINGS_PAGE = True
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN = False
        GlobalVars.OVERRIDE_SETTINGS_BTN = False
        
        GlobalVars.lastPageModule()

    def ButtonClick_RIGHTBTN(self):
        self.selected_character += 1
        self.UpdateChar()

    def ButtonHold_RIGHTBTN(self):
        self.setKeyb()
        time.sleep(0.1)

    def ButtonClick_LEFTBTN(self):
        self.rmvChar()

    def ButtonClick(self):
        self.addChar()

    def ButtonHold(self):
        self.setX()