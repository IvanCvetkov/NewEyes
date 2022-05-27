from skimage.filters import threshold_local
from google_speech import Speech
from image_processing import *
import numpy as np
import argparse
import cv2
import imutils
# construct the argument parser and parse the arguments
import numpy as np
import os
import cv2


def text_recognition(IMAGE_PATH):
    
    kill_mpg()

    language = ''
    os.environ['OMP_THREAD_LIMIT'] = '1'
    os.system("mpg321 /home/pi/please_wait.mp3 &")

    
    osd = ''
    try:
        osd = pytesseract.image_to_osd('/home/pi/scanned_receipt.jpg', config='--psm 0 -c min_characters_to_try=20')
        print(osd)
    except:
        pass
        
    if "Script: Cyrillic" in osd:
        language = 'bul'
    elif "Script: Latin" in osd:
        language = 'eng'
    else:
        language = 'eng'
    # Dewarp code goes here...
    
    text = receipt_text_extraction('/home/pi/scanned_receipt.jpg', language)
    text = mistake_removal(text)
    print(str(text))
    
    
    if 'bul' in language:
        language = 'bg'
    elif 'eng' in language:
        language = 'en'
        
    Speak(str(text), language)
    

def kill_mpg():
    os.system("pkill mpg321")
    
    
def Speak(text, language):
    
    if text != "":
        speech = Speech(text, language)
        speech.save("page.mp3")
        os.system('mpg321 page.mp3 &')

    else:
        errorMessages = ["ocr_error_1.mp3",
                         "ocr_error_2.mp3",
                         "ocr_error_3.mp3"]

        chosen_message = random.choice(errorMessages)
        print(chosen_message)

        os.system('mpg321 ' + '/home/pi/error_messages/' + chosen_message + ' &')


def scan_receipt():
    
    file_name = "/home/pi/Desktop/output-1.jpg"
    
    def order_points(pts):
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    def four_point_transform(image, pts):
        rect = order_points(pts)
        (tl, tr, br, bl) = rect

        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        return warped

    image = cv2.imread(file_name)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)
    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    # show the original image and the edge detected image
    print("STEP 1: Edge Detection")

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break
    # show the contour (outline) of the piece of paper
    print("STEP 2: Find contours of paper")
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)

    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset = 10, method = "gaussian")
    warped = (warped > T).astype("uint8") * 255
    # show the original and scanned images
    print("STEP 3: Apply perspective transform")

    cv2.imwrite('/home/pi/scanned_receipt.jpg', warped)
    text_recognition('/home/pi/scanned_receipt.jpg')

