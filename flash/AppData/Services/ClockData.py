## TIME SETUP, DONT DELETE
import time, ntptime


class Time:
    def __init__(self):
        self.ready = True

    def getTime(self):
        if self.ready:
            tm = time.localtime()
            return tm

    def getClock(self):
        if self.ready:
            tm = time.localtime()
            minutes = tm[3]
            seconds = tm[4]

            clock = f"{tm[3]:02d}:{tm[4]:02d}"
            return clock

    def localtime_tz(self, offset_hours=0):
        saved_utc = FileManager.search("UTC")
        if saved_utc != "none":
            utc = int(saved_utc)
            return time.localtime(utc + offset_hours * 3600)
        else:
            return time.localtime(time.time() + offset_hours * 3600)