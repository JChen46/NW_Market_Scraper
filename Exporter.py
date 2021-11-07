import csv
from datetime import datetime

def Exporter(totalRows):
    fields = ['Item', 'Average Price', 'Average Availability', 'Lowest Price', 'Date']

    # Get date for filename
    date = datetime.now()
    fileName = date.strftime("%m-%d-%Y_%H;%M")

    try:
        # Save to csv format
        with open('reports/'+fileName, 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(totalRows)
        print('Success! Report saved in reports/{}'.format(fileName), flush=True)
    except Exception as e:
        print(e)
        print('ERROR: Unable to save rows to reports, totalRows: {}'.format(totalRows), flush=True)

# Exporter([['iron ore', 0.21, 757.2, 0.2, '11/06/2021 15:09']]) # DEBUG