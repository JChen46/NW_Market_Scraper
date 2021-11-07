import pyautogui
import pydirectinput
import pytesseract
import cv2
from config import *
from time import sleep
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = 'C:/Users/John Chen/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'


def Searcher(keyword):  # Searches in market for keyword, returns true if found and selected
    pyautogui.moveTo(searchBarLocation)
    pyautogui.leftClick(searchBarLocation)

    # For some reason pyautogui doesn't work with shortcuts in NW
    pydirectinput.keyDown('ctrl')
    pydirectinput.press('a')
    pydirectinput.keyUp('ctrl')
    pyautogui.press('backspace')
    pyautogui.write(keyword)
    sleep(1.5)
    keyword_coordinates = SearchParser(keyword) # get coordinate of keyword
    if keyword_coordinates is not None:
        pyautogui.moveTo(keyword_coordinates)
        pyautogui.leftClick(keyword_coordinates)
        return True
    return False


def SearchParser(keyword, retries = 0):  # Selects keyword from search results, scrolls down if not found
    pyautogui.screenshot('temp1.png', region=(
        searchNWCoordinate + searchBoxSize))
    image = cv2.imread('temp1.png')
    height, width, channels = image.shape

    # Grayscale, Gaussian blur, Otsu's threshold
    greyImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blurImg = cv2.GaussianBlur(greyImg, (3, 3), 0)
    upscaledImg = cv2.resize(greyImg, (width*2, height*2), interpolation=cv2.INTER_CUBIC)

    threshImg = cv2.threshold(upscaledImg, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    invertedImg = 255 - threshImg

    # DEBUG - show invert img
    # cv2.imshow('invert', invertedImg)
    # cv2.imshow('upscaled', upscaledImg)
    # cv2.waitKey()

    results = pytesseract.image_to_data(
        invertedImg, config='--psm 6', output_type=Output.DICT)
    print(results["text"], flush=True) # DEBUG
    # print(len(results["text"]), flush=True) # DEBUG


    keyword_index = FindKeywordIndex(results, keyword)
    keyword_len = len(keyword.split(' '))
    if keyword_index is not None:
        # Find center position of desired keyword
        x_center = 0
        y_center = 0
        for i in range(keyword_len):
            x_center += results["left"][keyword_index+i] + results["width"][keyword_index+i]
            y_center += results["top"][keyword_index+i] + results["height"][keyword_index+i]
        print(x_center)
        x_center = x_center/keyword_len+searchNWCoordinate[0]
        print(x_center)
        y_center = y_center/keyword_len+searchNWCoordinate[1]
        print('Found keyword at: ({},{})'.format(x_center, y_center), flush=True)
        return (x_center, y_center)
    elif retries < max_retries:
        # Scroll down search list
        pyautogui.moveTo(x=searchBarDropDown[0], y=searchBarDropDown[1])
        pyautogui.scroll(-600) # scroll down 600 clicks
        sleep(0.2)
        print('Unable to find keyword, scrolling and retrying: {}'.format(retries+1), flush=True)
        SearchParser(keyword, retries+1)
    else:
        print('ERROR: {} retries exhausted, unable to find keyword {}'.format(retries, keyword), flush=True)
        return None




def FindKeywordIndex(results, keyword):
    keywords = keyword.lower().split(" ")
    result_len = len(results["text"])
    for i in range(result_len):
        results["text"][i] = results["text"][i].lower()

    for i in range(result_len):
        if results["text"][i] == keywords[0] and len(keywords) > 1:
            valid_index = True
            for j in range(len(keywords)):
                if results["text"][i+j] != keywords[j]:
                    valid_index = False
            if valid_index:
                if (i-2 < 0 or results["text"][i-2] == '') and (i+len(keywords) >= result_len or results["text"][i+len(keywords)] == ''):
                    return i
        elif results["text"][i] == keywords[0] and len(keywords) == 1:
            if results["text"][i-2] == '' and (i+1 >= result_len or results["text"][i+1] == ''):
                return i
                # if i+1 >= result_len:
                #     return i
                # elif results["text"][i+1] == '':
                #     return i
    return None


# SearchParser('recipe: blueberry pie')  # DEBUG testing

# results = {'text': ['brilliant', 'diamond']}
# print(len(results['text']))
# FindKeywordIndex(results["text"], 'brilliant diamond') #errors out 
