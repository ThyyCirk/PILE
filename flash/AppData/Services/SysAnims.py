import M5, time
from M5 import *
import GlobalVars
import _thread

ChargeAnim_Frames = [
    '/flash/res/img/ChargingImgs/1.png',
    '/flash/res/img/ChargingImgs/2.png',
    '/flash/res/img/ChargingImgs/3.png',
    '/flash/res/img/ChargingImgs/4.png',
]

class sysAnims():
    lock = _thread.allocate_lock()
    
    def __init__(self):
        self.animation_gen = None
        self.wait_until = 0
    
    def __call__(self, animation=None):
        if not animation or not hasattr(self, animation):
            return
        
        self.animation_gen = getattr(self, animation)()
        self.wait_until = 0

    def ChargeAnim(self):
        for frame in ChargeAnim_Frames:
            M5.Lcd.drawPng(frame, 0, 0)
            yield 250
        
        GlobalVars.lastPageModule()

    def tick(self):
        if self.animation_gen:
            if time.ticks_ms() < self.wait_until:
                return

            try:
                delay_ms = next(self.animation_gen)
                
                if isinstance(delay_ms, (int, float)):
                    self.wait_until = time.ticks_add(time.ticks_ms(), int(delay_ms))
                else:
                    self.wait_until = 0
                    
            except StopIteration:
                self.animation_gen = None