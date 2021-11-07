import pyautogui
from config import *
from time import sleep

def Settlements(): # Selects all settlements from dropdown
    pyautogui.moveTo(settlementDropdownLocation)
    pyautogui.leftClick(settlementDropdownLocation)
    pyautogui.move(xOffset=0, yOffset=45) # move to box area
    sleep(0.3)
    pyautogui.scroll(800)
    pyautogui.moveTo(settlementDropdownLocation[0], settlementDropdownLocation[1]+45)
    pyautogui.leftClick(settlementDropdownLocation[0], settlementDropdownLocation[1]+45)
    pyautogui.moveTo(settlementDropdownLocation)
    pyautogui.leftClick(settlementDropdownLocation)

# Settlements()