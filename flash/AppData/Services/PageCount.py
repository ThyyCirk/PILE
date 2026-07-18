from M5 import Display
import GlobalVars
import EventLitsener

class Draw:
    def __init__(self):
        self.draw_pos = "Down"
        self.page_count = 1
        self.current_page = 1
        
        self.x = 135
        self.y = 240
        self.w = 5
        self.h = 50
        self.r = 3
        
        self.pillSizeX = self.w
        self.pillSizeY = self.h
        self.pillX = self.x
        self.pillY = self.y
    
    def d(self):
        if self.draw_pos == "Left":
            self.h = 50
            self.w = 5
            self.y = 125 - self.h // 2
            self.x = 5

            self.pillSizeX = self.w
            self.pillSizeY = self.h // self.page_count

            self.pillX = self.x
            self.pillY = self.y + self.current_page * self.pillSizeY
        elif self.draw_pos == "Down":
            self.h = 5
            self.w = 50
            self.y = 230
            self.x = 135 // 2 - self.w // 2

            self.pillSizeX = self.w // self.page_count
            self.pillSizeY = self.h

            self.pillX = self.x + self.current_page * self.pillSizeX
            self.pillY = self.y
        else:
            return

        Display.fillRoundRect(
                self.x,
                self.y,
                self.w,
                self.h,
                self.r,
                0x555555
            )

        Display.fillRoundRect(
            self.pillX,
            self.pillY,
            self.pillSizeX,
            self.pillSizeY,
            self.r,
            0xFFFFFF
        )

    def setup(self, draw_pos=None, page_count=None):
        if draw_pos is not None:
            self.draw_pos = draw_pos
        if page_count is not None:
            self.page_count = page_count
            
        self.d()
    
    def update(self, current_page=None):
        self.current_page = current_page if current_page is not None else GlobalVars.currentPageModule_Index
        self.d()