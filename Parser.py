import pytesseract
import cv2
import pyautogui
import numpy
import re
import uuid

pytesseract.pytesseract.tesseract_cmd = 'C:/Users/John Chen/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'

def Parser(NWCoordinate, boxSize): # Parses string from image and returns as array
    pyautogui.screenshot('temp.png', region=(NWCoordinate + boxSize))
    image = cv2.imread('temp.png')
    height, width, channels = image.shape
    greyImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurImg = cv2.GaussianBlur(greyImg, (3,3), 0)
    diffImg = blurImg * -1 * greyImg
    tempDiff = diffImg.astype(numpy.uint16)
    upscaledImg = cv2.resize(tempDiff, (width*2, height*2), interpolation=cv2.INTER_AREA)

    # # Multiple methods of thresholding, not consistently clean, so leaving it here for documentation
    # threshImg = cv2.threshold(upscaledImg, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] # old method
    # threshImg = cv2.threshold(upscaledImg, 220, 255, cv2.THRESH_BINARY_INV)[1]
    # threshImg = cv2.adaptiveThreshold(greyImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5) # Gaussian version of adaptive thresholding
    # threshImg = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 4) # Gaussian version of adaptive thresholding
    # invert = 255 - threshImg

    raw_result = pytesseract.image_to_string(upscaledImg, config='--psm 6') # psm 6 for single digit recognition
    
    processed_result = raw_result.split()
    # Validate processed_result
    if not ValidateResult(processed_result, image):
        return None 

    print("processed: {}".format(processed_result), flush=True)
    
    # DEBUG - show images
    # cv2.imshow('grey', greyImg)
    # cv2.imshow('blur', blurImg)
    # cv2.imshow('diff', diffImg)
    # cv2.imshow('upscaled', upscaledImg)
    # cv2.imshow('tempdiff', 255 - tempDiff)
    # cv2.imshow('invert', threshImg)
    # cv2.waitKey()
    return processed_result

def ValidateResult(result, tempImg):
    valid = True
    print(len(result),flush=True)
    for i in result:
        if re.search(r'[^0-9.]', i):
            valid = False

    if not valid or len(result) != 5:
        print('ERROR: Invalid result found: \n{}'.format(result), flush=True)
        # Log invalid image and results
        file_name = 'invalid_images/'+str(uuid.uuid4())+'.png'
        with open(file_name+'.txt', 'w') as f:
            f.write('\n'.join(result))
        cv2.imwrite(file_name, tempImg)
        print('Saved invalid result to invalid_images as {}'.format(file_name), flush=True)
        return False
    return True

# Parser((2096, 442), (80, 483)) # run parser on availability section
# Parser((1300, 442), (165, 483))