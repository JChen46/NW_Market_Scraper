import pyautogui
import winsound
from time import sleep
from config import *
from Parser import Parser
from Searcher import Searcher
from Settlements import Settlements
from ProcessRow import ProcessRow
from Exporter import Exporter

def Main():
    totalRows = []

    # Kooky starting jingle sound
    print("Starting script...", flush=True)
    for i in range(4):
        if i == 3:
            winsound.Beep(698, 500)
        else:
            winsound.Beep(349, 250)
        sleep(0.3)

    # Set markets to all settlements
    if all_settlements:
        print("Selecting all settlements...", flush=True)
        Settlements()

    for keyword in keywords:
        # Search for iteration item
        print('Searching for item: {}'.format(keyword), flush=True)
        searchKeyword = Searcher(keyword)

        # Validate search result
        if not searchKeyword:
            continue

        # Get values from market
        priceList = Parser(priceNWCoordinate, priceBoxSize)
        availList = Parser(availabilityNWCoordinate, availabilityBoxSize)

        # Validate parsed lists
        if priceList is None or availList is None:
            continue

        # Add results to totalRows
        print('Processing row...', flush=True)
        totalRows.append(ProcessRow(keyword, priceList, availList))

    # Save results to csv in /reports
    print('Saving results...', flush=True)
    Exporter(totalRows)


#  # Extra references
# pyautogui.press('space')
# pyautogui.write('hello world!', 0.25)
# screenWidth, screenHeight = pyautogui.size() # Returns two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)
# currentMouseX, currentMouseY = pyautogui.position() # Returns two integers, the x and y of the mouse cursor's current position.

Main()
print("\nScript ended.")