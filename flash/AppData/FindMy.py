import M5
from M5 import *
from SaveFileModule import FileManager
import GlobalVars
import math
import random

class FindMy:
    def __init__(self):
        self.FindMyPage_LOOP_FUNCTIONS = {
            0: self.intro_Animation,
            1: self.approxLocaation_animation,
            2: self.INTO_ARROW,
            3: self.lookForPhone,
        }
        self.FindMyPageNum = 0
        self.circles = []
        self.pivot_x = 67
        self.pivot_y = 112
        
        # State tracking variables for animations
        self.into_called = False
        self.frame = 0
        
        self.FindMyPage()
    
    def __load__(self):
        self.circles.clear()
        self.into_called = False
        self.frame = 0
        
        self.FindMyPage()

    def FindMyPage(self):
        GlobalVars.topBarVisible = True
        
        M5.Lcd.clear(0x000000)
        
        for _ in range(20):
            self.spawn_circle()
            
        self.tick()

    def spawn_circle(self):
        dist = random.randint(35, 45)      # distance from pivot
        r = random.randint(1, 5)           # circle radius
        spin = random.uniform(0.1, 0.5)    # degrees per frame, small = slow
        angle = random.uniform(0, 360)     # initial angle
        self.circles.append([dist, r, spin, angle])

        # Draw initial circle
        x = int(self.pivot_x + dist * math.cos(math.radians(angle)))
        y = int(self.pivot_y + dist * math.sin(math.radians(angle)))
        M5.Lcd.fillCircle(x, y, r, 0xFFFFFF)

    def get_pos(self, dist, angle):
        rad = math.radians(angle)
        x = self.pivot_x + dist * math.cos(rad)
        y = self.pivot_y + dist * math.sin(rad)
        return int(x), int(y)

    def intro_Animation(self):
        M5.Lcd.setTextSize(2)
        M5.Lcd.setTextColor(0xFFFFFF, 0X000000)
        M5.Lcd.setCursor(40, 200)
        M5.Lcd.print("Find?")
        for c in self.circles:
            dist, r, spin, angle = c

            # Erase old position
            x, y = self.get_pos(dist, angle)
            M5.Lcd.fillCircle(x, y, r, 0x000000)

            # Update angle
            angle += spin
            if angle >= 360:
                angle -= 360
            c[3] = angle

            # Draw new position
            x, y = self.get_pos(dist, angle)
            M5.Lcd.fillCircle(x, y, r, 0xFFFFFF)
    
    def INTO_ARROW(self):
        if not self.into_called:
            self.into_called = True
        else:
            return 0
            
        frames = [
            '/flash/res/img/FindMyArrowIntroAnim/1.png',
            '/flash/res/img/FindMyArrowIntroAnim/2.png',
            '/flash/res/img/FindMyArrowIntroAnim/3.png',
            '/flash/res/img/FindMyArrowIntroAnim/4.png',
        ]
        pos = 0
        while pos < 35:
            for c in self.circles:
                dist, r, spin, angle = c

                # Erase old position
                x, y = self.get_pos(dist, angle)
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
                x, y = self.get_pos(dist, angle)
                M5.Lcd.fillCircle(x, y, r, 0xFFFFFF)
                
            if pos >= 31:
                M5.Lcd.drawPng(frames[self.frame], self.pivot_x - 25, self.pivot_y - 25)
                self.frame += 1
            pos += 1
        
        for c in self.circles:
            dist, r, spin, angle = c
            x, y = self.get_pos(dist, angle)
            M5.Lcd.fillCircle(x, y, r, 0x000000)
            
        M5.Lcd.drawPng('/flash/res/img/FindMyArrowIntroAnim/4.png', self.pivot_x - 25, self.pivot_y - 25)
        self.FindMyPageNum = 3
    
    def approxLocaation_animation(self):
        M5.Lcd.setTextSize(2)
        M5.Lcd.setTextColor(0xFFFFFF, 0X000000)
        M5.Lcd.setCursor(0, 200)
        M5.Lcd.print("Locating \nphone...")
        
        ax, ay, az = tuple(round(x, 3) for x in M5.Imu.getAccel())
        
        for c in self.circles:
            dist, r, spin, angle = c

            # Erase old position
            x, y = self.get_pos(dist, angle)
            M5.Lcd.fillCircle(x, y, r, 0x000000)
            c[2] = ax
            
            # Update angle
            angle += ax  # Using the updated spin from IMU here
            if angle >= 360:
                angle -= 360
            c[3] = angle

            # Draw new position
            x, y = self.get_pos(dist, angle)
            M5.Lcd.fillCircle(x, y, r, 0xFFFFFF)
            
    def lookForPhone(self):
        self.frame = 0
        self.into_called = False
        return 0
        
    def tick(self):
        self.FindMyPage_LOOP_FUNCTIONS[self.FindMyPageNum]()

    def ButtonClick(self):
        if self.FindMyPageNum == 0:
            self.FindMyPageNum = 1
        elif self.FindMyPageNum == 1:
            self.FindMyPageNum = 2