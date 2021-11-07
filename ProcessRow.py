import csv
from datetime import datetime

def ProcessRow(keyword, priceList, availabilityList):
    # Convert lists to float lists
    processedPriceList = [float(i) for i in priceList]
    processedAvailabilityList = [float(i) for i in availabilityList]

    # Get lowest price
    lowestPrice = min(processedPriceList)

    # Get Averages
    priceAverage = sum(processedPriceList)/len(processedPriceList)
    availabililtyAverage = sum(processedAvailabilityList)/len(processedAvailabilityList)

    # Get date for filename
    date = datetime.now()
    formattedDate = date.strftime("%m/%d/%Y %H:%M")

    # Compose Row
    processedRow = [keyword, round(priceAverage, 2), round(availabililtyAverage, 2), lowestPrice, formattedDate]
    # print(processedRow) # DEBUG
    return processedRow

# ProcessRow('iron ore', ['1', '2', '3', '4'], ['1', '2', '4', '1']) # DEBUG

