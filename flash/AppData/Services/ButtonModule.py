import M5
from M5 import BtnA, BtnB, BtnPWR
import GlobalVars
import AppsModule
import _thread

draw_anim = None 

def setup():
    BtnA.setHoldThresh(200)
    BtnB.setHoldThresh(200)
    BtnPWR.setHoldThresh(200)

from QuickSettings import QuickSettings as QS
def QuickSettings():
    GlobalVars.quickOpen = not GlobalVars.quickOpen

    if GlobalVars.quickOpen:
        GlobalVars.currentPageModule = QS()
    else:
        GlobalVars.currentPageModule.close()
        
def PageSelection():
    GlobalVars.currentPageModule = AppsModule.Apps()
    
def changepage(_next=True):
    AppsModule.changepage(_next)

def dispatch(page_module, method_name):
    """Small helper to cut down on repeated hasattr/getattr boilerplate."""
    fn = getattr(page_module, method_name, None)
    if fn is not None:
        fn()

def tick():
    page = GlobalVars.currentPageModule

    if hasattr(page, "tick"):
        page.tick()

    # ─── BtnA ──────────────────────────────────────────────
    if BtnA.isHolding():
        dispatch(page, "ButtonHold")

    if BtnA.wasHold():
        dispatch(page, "wasHold")

    if BtnA.wasSingleClicked():
        dispatch(page, "ButtonClick")

    if BtnA.wasDoubleClicked():
        dispatch(page, "ButtonDoubleClick")

    # ─── BtnB ──────────────────────────────────────────────
    if BtnB.wasSingleClicked():
        if GlobalVars.ALLOW_NEXT_PAGE:
            changepage()
        elif GlobalVars.OVERRIDE_NEXT_PAGE_BTN:
            dispatch(page, "ButtonClick_RIGHTBTN")
        return   # skip remaining checks this frame

    if BtnB.wasDoubleClicked():
        dispatch(page, "ButtonDoubleClick_RIGHTBTN")
        return

    if BtnB.isHolding():
        if GlobalVars.OVERRIDE_NEXT_PAGE_BTN:
            dispatch(page, "ButtonHold_RIGHTBTN")
        else:
            PageSelection()
        return

    # ─── BtnPWR ────────────────────────────────────────────
    if BtnPWR.wasSingleClicked():
        if GlobalVars.ALLOW_SETTINGS_PAGE:
            QuickSettings()
        elif GlobalVars.OVERRIDE_SETTINGS_BTN:
            dispatch(page, "ButtonClick_LEFTBTN")
        return

    if BtnPWR.wasDoubleClicked():
        dispatch(page, "ButtonDoubleClick_LEFTBTN")
        return

page_config={}

def draw():
    global page_config
    if not page_config:
        return
    page = GlobalVars.currentPageModule
    pageNum = GlobalVars.currentPageModule_Index
    
    x = 0
    y = 0
    
    events = page_config.get(pageNum, {})
    default = page_config[10]

    if not GlobalVars.OVERRIDE_NEXT_PAGE_BTN:
        default.update({"ButtonClick_RIGHTBTN": "ArrowRight"})
    if not GlobalVars.OVERRIDE_SETTINGS_BTN:
        default.update({"ButtonClick_LEFTBTN": "Circle"})

    # merge: page-specific events take priority over defaults
    merged = default.copy()
    merged.update(events)

    btnA_events = {k: v for k, v in merged.items() if not k.endswith("_LEFTBTN") and not k.endswith("_RIGHTBTN")}
    btnPWR_events = {k.replace("_LEFTBTN", ""): v for k, v in merged.items() if k.endswith("_LEFTBTN")}
    btnB_events = {k.replace("_RIGHTBTN", ""): v for k, v in merged.items() if k.endswith("_RIGHTBTN")}
    
    x = 135//2 - len(btnA_events) * 5
    y = 230
    for event_name, sprite in btnA_events.items():
        M5.Lcd.fillRect(x, y, 10, 10, 0x000000)
        M5.Lcd.drawPng(
            f"/flash/res/img/ButtonModule_Sprites/{event_name}.png",
            x,
            y,
            0, 0,
            0, 0,
            1, 1
        )
        if sprite != "":
            M5.Lcd.fillRect(x, y - 10, 10, 10, 0x000000)
            M5.Lcd.drawPng(
                f"/flash/res/img/ButtonModule_Sprites/{sprite}.png",
                x,
                y - 10,
                0, 0,
                0, 0,
                1, 1
            )
        x+=10
    
    x = 125
    y = 120 - len(btnB_events) * 5
    for event_name, sprite in btnB_events.items():
        M5.Lcd.fillRect(x, y, 10, 10, 0x000000)
        M5.Lcd.drawPng(
            f"/flash/res/img/ButtonModule_Sprites/{event_name}.png",
            x,
            y,
            0, 0,
            0, 0,
            1, 1
        )
        if sprite != "":
            M5.Lcd.fillRect(x - 10, y, 10, 10, 0x000000)
            M5.Lcd.drawPng(
                f"/flash/res/img/ButtonModule_Sprites/{sprite}.png",
                x - 10,
                y,
                0, 0,
                0, 0,
                1, 1
            )
        y+=10
    
    x = 0
    y = 230
    for event_name, sprite in btnPWR_events.items():
        M5.Lcd.fillRect(x, y, 10, 10, 0x000000)
        M5.Lcd.drawPng(
            f"/flash/res/img/ButtonModule_Sprites/{event_name}.png",
            x,
            y,
            0, 0,
            0, 0,
            1, 1
        )
        if sprite != "":
            M5.Lcd.fillRect(x + 10, y, 10, 10, 0x000000)
            M5.Lcd.drawPng(
                f"/flash/res/img/ButtonModule_Sprites/{sprite}.png",
                x + 10,
                y,
                0, 0,
                0, 0,
                1, 1
            )
        y-=10
        
def clearPages():
    page_config.clear()

def setupPages(pc=None):
    global page_config
    
    if pc is None:
        page = GlobalVars.currentPageModule
        possible = ["ButtonClick", "ButtonHold", "ButtonDoubleClick"]
        left_add = "_LEFTBTN"
        right_add = "_RIGHTBTN"

        detected = {}
        for name in possible:
            if hasattr(page, name):
                detected[name] = ""
        for name in possible:
            suffixed = name + left_add
            if hasattr(page, suffixed):
                detected[suffixed] = ""
        for name in possible:
            suffixed = name + right_add
            if hasattr(page, suffixed):
                detected[suffixed] = ""

        page_config = {10: detected}
    else:
        page_config = pc
        if 10 not in page_config:
            page_config[10] = {}