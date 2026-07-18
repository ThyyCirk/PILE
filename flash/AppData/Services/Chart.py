## Chart creator
    ### ROW COLOR [POSITION, CLRS...] POSITION = false --> left; true --> right
import M5
from M5 import *

def draw(
    rows,
    cols,
    x=0,
    y=0,
    h=40,
    w=121,
    rowColors=None,
    columnColors=None,
    rowLetters=None,
    columnLetters=None,
    sortBy=None,
    AddIntoCells=None,
    size=4
    ):
    
    localX, localY = x, y
    Column_Spacing = w // (cols - 1)
    Row_Spacing = h // (rows - 1)
    
    ## COLUMN CREATION
    for i in range(0, cols):
        if columnColors != None:
            if columnColors[0] == False:
                color = columnColors[i + 1] if i+1 < len(columnColors) else columnColors[1]
                M5.Lcd.fillEllipse(localX, y - size * 3, size, size, color)
            else:
                color = columnColors[i + 1] if i+1 < len(columnColors) else columnColors[1]
                M5.Lcd.fillEllipse(localX, y + h + size * 3, size, size, color)
        
        if columnLetters != None:
            if columnLetters[0] == False:
                letter = columnLetters[i + 1] if i+1 < len(columnLetters) else columnLetters[1]
                M5.Lcd.setTextSize(0.85)
                M5.Lcd.setTextColor(0xFFFFFF, 0X000000)
                M5.Lcd.setCursor(localX - len(letter) * 2, y - size * 2)
                M5.Lcd.print(letter)
            else:
                letter = columnLetters[i + 1] if i+1 < len(columnLetters) else columnLetters[1]
                M5.Lcd.setTextSize(0.85)
                M5.Lcd.setTextColor(0xFFFFFF, 0X000000)
                M5.Lcd.setCursor(localX - len(letter) * 2, y + h + size * 2)
                M5.Lcd.print(letter)
            
        M5.Lcd.drawLine(localX, y, localX, y + h, 0xBBBBBB)
        localX += Column_Spacing
    
    ## ROW CREATION
    for i in range(0, rows):
        if rowColors != None:
            if rowColors[0] == False:
                color = rowColors[i+1] if i+1 < len(rowColors) else rowColors[0]
                M5.Lcd.fillEllipse(x - size * 3, localY, size, size, color)
            else:
                color = rowColors[i+1] if i+1 < len(rowColors) else rowColors[0]
                M5.Lcd.fillEllipse(x + w + size * 3, localY, size, size, color)
                
            if rowLetters != None:
                if rowLetters[0] == False:
                    letter = rowLetters[i + 1] if i+1 < len(rowLetters) else rowLetters[1]
                    M5.Lcd.setTextSize(0.85)
                    M5.Lcd.setCursor(x - size * 3, localY - len(letter))
                    M5.Lcd.print(letter)
                else:
                    letter = rowLetters[i + 1] if i+1 < len(rowLetters) else rowLetters[1]
                    M5.Lcd.setTextSize(0.85)
                    M5.Lcd.setCursor(x + w + size * 3, localY - len(letter))
                    M5.Lcd.print(letter)
        M5.Lcd.drawLine(x, localY, x + w, localY, 0xBBBBBB)
        localY += Row_Spacing
        
    ## DATA ADDING
    pos = [] ## (x, y)
    if sortBy:
        for i, (key, value, specialkey) in enumerate(sortBy):
            key = int(key) if key.isdigit() else specialkey
            localX = x + Column_Spacing * int(key)
            localY = y + Row_Spacing * int(value)
            M5.Lcd.fillEllipse(localX, localY, size - 1, size - 1, 0xAA0099)
            pos.append((localX, localY))
            
            if i > 0 and i < len(sortBy):
                M5.Lcd.drawLine(pos[i - 1][0], pos[i - 1][1], pos[i][0], pos[i][1], 0xAA0099)
    elif AddIntoCells:
        for i, (key, value, specialkey) in enumerate(sortBy):
            key = int(key) if key.isdigit() else specialkey
            localX = x + Column_Spacing * int(key)
            localY = y + Row_Spacing * int(value)