import pyautogui

# Keyword cannot be a header (ie. Resources, Apparel, etc.), and cannot be an item that is too long for search box
# Issue: sometimes cannot decipher between an I and a L
keywords = ['iron ore', 'brilliant diamond']

max_retries = 0

all_settlements = True

# numericalRegex = '[0-9.\n]'

searchBarLocation = (400,300)
searchBarDropDown = (400, 800)

settlementDropdownLocation = (2300, 200)

availabilityNWCoordinate = (2005, 442)
availabilityBoxSize = (80, 483)
# availabilitySECoordinate = (2100, 925)

priceNWCoordinate = (1300, 442)
priceBoxSize = (165, 483)
# priceSECoordinate = (1465, 925)

searchNWCoordinate = (140, 400)
searchBoxSize = (580, 600)
# searchSECoordinate = (720 1000)

screenSize = pyautogui.size() # unused atm