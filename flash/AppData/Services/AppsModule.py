## APP SELECTION /  MODULE, VERY IMPORTANT DONT DELETE

import M5, os, time
from M5 import *
import GlobalVars
from SaveFileModule import FileManager
import json

class Apps:
    def __init__(self, o=True):
        self.Pages = [f[:-3] for f in os.listdir('/flash/AppData') if f.endswith('.py')]
        self.AppFile = '/flash/libs/AppOrder.txt'
        
        self.Favourites = json.loads(FileManager.search('favourites', self.AppFile).replace("'", '"'))
        self.AllApps = json.loads(FileManager.search('all', self.AppFile).replace("'", '"'))
        
        self.sort_pages()
        self.check_for_new_apps()
        
        self.PageSelectedIndex = 0
        self.pageSelectionEntered = False
        
        # animations
        self.NextPage_Imgs = [
            '/flash/res/img/NextPageFrames/1.png',
            '/flash/res/img/NextPageFrames/2.png',
            '/flash/res/img/NextPageFrames/3.png',
            '/flash/res/img/NextPageFrames/4.png',
            '/flash/res/img/NextPageFrames/5.png',
            '/flash/res/img/NextPageFrames/6.png',
        ]
        self.SelectionPage_IntroFrames = [
            '/flash/res/img/SelectionPage_IntroFrames/2.png',
            '/flash/res/img/SelectionPage_IntroFrames/3.png',
            '/flash/res/img/SelectionPage_IntroFrames/4.png',
            '/flash/res/img/SelectionPage_IntroFrames/6.png',
            '/flash/res/img/SelectionPage_IntroFrames/7.png',
        ]

        self.PageGenie_Frames = [
            '/flash/res/img/PageGenie/1.png',
            '/flash/res/img/PageGenie/2.png',
            '/flash/res/img/PageGenie/3.png',
            '/flash/res/img/PageGenie/4.png',
            '/flash/res/img/PageGenie/5.png',
            '/flash/res/img/PageGenie/6.png',
        ]
        
        if o:
            GlobalVars.lastPageModule = GlobalVars.currentPageModule
            GlobalVars.currentPageModule = self
        
            self.PageSelection()
        
    def __call__(self, o=True):
        
        self.sort_pages()
        self.check_for_new_apps()
        
        if o:
            GlobalVars.lastPageModule = GlobalVars.currentPageModule
            GlobalVars.currentPageModule = self
            
            self.PageSelection()
        
    def PageSelection(self):
        GlobalVars.topBarVisible = False
        
        if not self.pageSelectionEntered:
            self.nextpage_overlay(True, self.SelectionPage_IntroFrames)
            self.pageSelectionEntered=True

            GlobalVars.ALLOW_NEXT_PAGE=False
            GlobalVars.ALLOW_SETTINGS_PAGE=False
            GlobalVars.OVERRIDE_NEXT_PAGE_BTN=True 
            
        if self.PageSelectedIndex > len(self.Pages) - 1:
            self.PageSelectedIndex = 0
        
        def PageList():
            y=0
            w=135
            h=25
            TextSize=1.5
            for i, page in enumerate(self.Pages):
                hasstar = False if page not in self.Favourites else True
                name = page.replace("_Page", "").replace(".py", "").replace("_page", "")
                if i != self.PageSelectedIndex:
                    M5.Lcd.drawRect(0, y, w, h, 0xff812f)
                    if not hasstar:
                        M5.Lcd.setCursor(0, y+5)
                    else:
                        M5.Lcd.drawPng('/flash/res/img/misc/StarUnsel.png', 2, y+5)
                        M5.Lcd.setCursor(13, y+5)
                    M5.Lcd.setTextSize(TextSize)
                    M5.Lcd.setTextColor(0xff812f, 0X000000)
                    M5.Lcd.print(f"{name}")
                else:
                    M5.Lcd.fillRect(0, y, w, h, 0xff812f)
                    if not hasstar:
                        M5.Lcd.setCursor(0, y+5)
                    else:
                        M5.Lcd.drawPng('/flash/res/img/misc/StarSel.png', 2, y+5)
                        M5.Lcd.setCursor(13, y+5)
                    M5.Lcd.setTextSize(TextSize)
                    M5.Lcd.setTextColor(0xFFFFFF, 0xff812f)
                    M5.Lcd.print(f"{name}")
                    
                y+=h
                    
        M5.Lcd.clear(0x000000)
        PageList()
    
    def nextpage_overlay(self, expand=True, imgList=None):
        if imgList == None:
            return
        frames = imgList if expand else list(reversed(imgList))
        for frame in frames:
            M5.Lcd.drawPng(frame, 0, 0)
            
    def ButtonClick_RIGHTBTN(self):
        self.PageSelectedIndex+=1
        self.PageSelection()

    def ButtonHold_RIGHTBTN(self):
        selPage=self.Pages[self.PageSelectedIndex]
        frames = self.PageGenie_Frames
            
        x = 0
        y = -240//2 + (self.PageSelectedIndex + 1)*25 - 5
        
        for i, frame in enumerate(frames):
            if i < 3:
                M5.Lcd.drawPng(frame, x, y)
            else:
                t = 0.25  # tween speed (0.1 slow → 0.4 fast)

                x = self.lerp(x, 0, t)
                y = self.lerp(y, 0, t)

                M5.Lcd.drawPng(frame, int(x), int(y))
        
        self.PageSelectedIndex = 0
        self.pageSelectionEntered = False
        GlobalVars.ALLOW_NEXT_PAGE = True 
        GlobalVars.ALLOW_SETTINGS_PAGE = True
        GlobalVars.OVERRIDE_NEXT_PAGE_BTN = False
        
        module = __import__(selPage)
        GlobalVars.currentPageModule = getattr(module, selPage)()
    
    def ButtonHold(self):
        selPage = self.Pages[self.PageSelectedIndex]
        
        if selPage not in self.Favourites:
            self.Favourites.append(selPage)
        else:
            self.Favourites.remove(selPage)
        
        FileManager.write('favourites', self.Favourites, self.AppFile)
        self()
    
    def lerp(self, a, b, t):
        return a + (b - a) * t
    
    def sort_pages(self):
        favourites = self.Favourites
        
        ordered = sorted([p for p in self.Pages if p in favourites])
        remaining = sorted([p for p in self.Pages if p not in favourites])
        
        self.Pages = ordered + remaining
    
    def check_for_new_apps(self):
        if len(self.Pages) != len(self.AllApps):
            FileManager.write('all', self.Pages, self.AppFile)
            
    def get_pages(self):
        self.check_for_new_apps()
        self.sort_pages()
        return self.Pages
    
    def get_page(self, pageName):
        module = __import__(pageName)
        GlobalVars.currentPageModule = getattr(module, selPage)()
            
    
def changepage(_next=True):
    current = type(GlobalVars.currentPageModule).__name__
    apps = Apps(False)
    pages = apps.get_pages()
    index = pages.index(current) if current in pages else 0
    currentPage = index

    if _next:
        currentPage += 1
        if currentPage >= len(apps.Pages):
            currentPage = 0
    else:
        currentPage -= 1
        if currentPage < 0:
            currentPage = len(apps.Pages) - 1
    
    Speaker.tone(1500, 5)
    apps.nextpage_overlay(True, apps.NextPage_Imgs)
    
    selPage = apps.Pages[currentPage]
    module = __import__(selPage)
    GlobalVars.currentPageModule = getattr(module, selPage)()