import os
from SupportMethods import *
from string import digits
import cv2
#from wand.image import Image
from textblob import TextBlob
import numpy as np
import pyttsx3
from imutils.perspective import four_point_transform
import imutils
from skimage.segmentation import clear_border
import pytesseract
import sys


def modifyImage(imageUrl):
    image = cv2.imread(imageUrl)
    #image.despeckle() # Reduces Noise Levels
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Binarization
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 87, 13)
    showImg(adaptive_threshold)
    return image

def extractText(image, language):
    # --psm1
    config = '-l eng --oem 1 --psm 3'
    text = pytesseract.image_to_string(image, config=config, lang=language)
    print(text)
    return text

def deskew(imageUrl, debug=False):
    image = cv2.imread(imageUrl)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 3)
    thresh = cv2.adaptiveThreshold(blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)

    if debug:
        cv2.imshow("Puzzle Thresh", thresh)
        cv2.waitKey(0)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    puzzleCnt = None

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            puzzleCnt = approx
            break
    if puzzleCnt is None:
        raise Exception(("Could not find sudoku puzzle outline. "
            "Try debugging your thresholding and contour steps."))

    if debug:
        output = image.copy()
        cv2.waitKey(0)

    puzzle = four_point_transform(image, puzzleCnt.reshape(4, 2))
    warped = four_point_transform(gray, puzzleCnt.reshape(4, 2))

    if debug:
        cv2.imshow("Puzzle Transform", puzzle)
        cv2.waitKey(0)

    return (puzzle, warped)

def removeMistakes(input):
    text = input.strip()
    text = text.replace("©", "")
    text = text.replace("|", "I")
    text = text.replace("1", "I")
    text = text.replace("[", "")
    text = text.replace("]", "")
    text = text.replace("{", "")
    text = text.replace("}", "")
    text = text.replace("\n", " ")
    text = ''.join(c if c not in map(str, range(0, 10)) else "" for c in text)
    textBlob = TextBlob(text)
    return textBlob

def textToSpeech(text):
    engine = pyttsx3.init()

    # rate = engine.getProperty('rate')
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 0.8)

    if text != "":
        message = "In front of you is: "
        engine.say(message + str(text))
        engine.runAndWait()

    else:
        errorMessage = "There is nothing in front of you!"
        engine.say(errorMessage)
        engine.runAndWait()